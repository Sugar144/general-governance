"""Deterministic, process-safe allocation of namespaced identities.

The allocator is deliberately stateful: an emitted identity is a durable
reservation, even if a caller later fails before publishing its artifact.
This makes identity reuse impossible without requiring a central service.
"""

from __future__ import annotations

from dataclasses import dataclass
import fcntl
import json
import os
from pathlib import Path
import re
import tempfile


_NAMESPACE = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)*$")
_KIND = re.compile(r"^[A-Z][A-Z0-9_]*$")
_IDENTITY = re.compile(r"^(?P<namespace>[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)*):(?P<kind>[A-Z][A-Z0-9_]*):(?P<sequence>[0-9]{6,})$")


class IdentityError(ValueError):
    """The allocation request or its durable state is invalid."""


@dataclass(frozen=True)
class Allocation:
    identity: str
    namespace: str
    kind: str
    sequence: int


def parse(identity: str) -> Allocation:
    match = _IDENTITY.fullmatch(identity)
    if not match:
        raise IdentityError(f"not a namespaced identity: {identity}")
    sequence = int(match["sequence"])
    if sequence < 1:
        raise IdentityError(f"identity sequence must be positive: {identity}")
    return Allocation(identity, match["namespace"], match["kind"], sequence)


def _validate(namespace: str, kind: str) -> None:
    if not _NAMESPACE.fullmatch(namespace):
        raise IdentityError(f"invalid namespace: {namespace}")
    if not _KIND.fullmatch(kind):
        raise IdentityError(f"invalid identity kind: {kind}")


def _read_state(path: Path, namespace: str) -> dict:
    if not path.exists():
        return {"schema_version": "0.1.0", "namespace": namespace, "next_sequences": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IdentityError(f"cannot read allocator state {path}: {exc}") from exc
    if set(state) != {"schema_version", "namespace", "next_sequences"} or state["schema_version"] != "0.1.0":
        raise IdentityError(f"invalid allocator state shape: {path}")
    if state["namespace"] != namespace or not isinstance(state["next_sequences"], dict):
        raise IdentityError(f"allocator state namespace mismatch: {path}")
    for kind, next_sequence in state["next_sequences"].items():
        _validate(namespace, kind)
        if not isinstance(next_sequence, int) or next_sequence < 1:
            raise IdentityError(f"invalid next sequence for {kind}: {path}")
    return state


def _atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        temporary_path.unlink(missing_ok=True)


class Allocator:
    """One namespace authority backed by a local atomic state file.

    Calls serialize on ``state_path``'s sibling lock.  State is advanced before
    the append-only ledger is written, so a crash may leave a gap but can never
    recycle an already emitted identity.
    """

    def __init__(self, *, namespace: str, state_path: str | Path, ledger_path: str | Path):
        _validate(namespace, "ID")
        self.namespace = namespace
        self.state_path = Path(state_path)
        self.ledger_path = Path(ledger_path)
        self.lock_path = self.state_path.with_name(f".{self.state_path.name}.lock")

    def peek(self, kind: str) -> Allocation:
        """Return a non-reserving preview without creating allocator state.

        A preview is advisory under concurrent writers; callers must use
        ``allocate`` before publishing an identity.
        """
        _validate(self.namespace, kind)
        state = _read_state(self.state_path, self.namespace)
        sequence = state["next_sequences"].get(kind, 1)
        return self._allocation(kind, sequence)

    def allocate(self, kind: str, *, purpose: str) -> Allocation:
        _validate(self.namespace, kind)
        if not isinstance(purpose, str) or not purpose.strip():
            raise IdentityError("allocation purpose is required")
        with self._locked():
            state = _read_state(self.state_path, self.namespace)
            sequence = state["next_sequences"].get(kind, 1)
            allocation = self._allocation(kind, sequence)
            state["next_sequences"][kind] = sequence + 1
            _atomic_json(self.state_path, state)
            self._append_ledger(allocation, purpose)
            return allocation

    def _allocation(self, kind: str, sequence: int) -> Allocation:
        if sequence > 999999:
            raise IdentityError(f"identity space exhausted for {self.namespace}:{kind}")
        identity = f"{self.namespace}:{kind}:{sequence:06d}"
        return Allocation(identity, self.namespace, kind, sequence)

    def _append_ledger(self, allocation: Allocation, purpose: str) -> None:
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "identity": allocation.identity,
            "kind": allocation.kind,
            "purpose": purpose,
            "schema_version": "0.1.0",
            "sequence": allocation.sequence,
        }
        try:
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
        except OSError as exc:
            raise IdentityError(f"identity reserved but ledger append failed: {allocation.identity}: {exc}") from exc

    class _Lock:
        def __init__(self, path: Path):
            self.path = path
            self.handle = None

        def __enter__(self):
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.handle = self.path.open("a+", encoding="utf-8")
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX)
            return self

        def __exit__(self, exc_type, exc, traceback):
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()

    def _locked(self):
        return self._Lock(self.lock_path)


def resolve_historical(identity: str, forward_mapping: dict[str, str]) -> str:
    """Resolve an exact historical reference through an optional forward map.

    The input is never rewritten.  Mapping targets must be namespaced IDs and
    no namespaced ID may be mapped again, preventing translation chains.
    """
    for historical, target in forward_mapping.items():
        if not isinstance(historical, str) or not isinstance(target, str):
            raise IdentityError("historical forward mapping must contain string identities")
        try:
            parse(historical)
        except IdentityError:
            pass
        else:
            raise IdentityError(f"forward mapping key is already namespaced: {historical}")
        parse(target)
    if identity in forward_mapping:
        target = forward_mapping[identity]
        parse(target)
        return target
    return identity
