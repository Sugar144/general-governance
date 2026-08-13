"""Fail-closed delegated operational authority for bounded L6 effects.

This is deliberately a small guard, not an IAM system.  Callers present an
explicit authority object and a bounded request; the effect callback is only
invoked after a deterministic authorization decision has been audit-recorded.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path, PurePosixPath
from typing import Callable, Mapping, Sequence, TypeVar


AUTHORIZED = "AUTHORIZED"
DENIED = "DENIED"
INDETERMINATE = "INDETERMINATE"
_STATES = {AUTHORIZED, DENIED, INDETERMINATE}
_T = TypeVar("_T")


class AuthorityError(ValueError):
    """The supplied authority or request is not a valid bounded input."""


@dataclass(frozen=True)
class Authorization:
    principal: str
    context: str
    allowed_actions: tuple[str, ...]
    allowed_paths: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    constraints: Mapping[str, str]
    provenance: str
    expires_at: str | None = None


@dataclass(frozen=True)
class Request:
    actor: str
    context: str
    action: str
    paths: tuple[str, ...]


@dataclass(frozen=True)
class Decision:
    state: str
    requested_action: str
    authority_presented: str
    boundary: str
    retry_with_new_authority: bool


def _nonempty(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AuthorityError(f"{field} must be a non-empty string")
    return value


def _safe_relative(path: str) -> PurePosixPath:
    path = _nonempty(path, "path")
    value = PurePosixPath(path)
    if value.is_absolute() or ".." in value.parts or str(value) == ".":
        raise AuthorityError(f"path is not a bounded relative path: {path}")
    return value


def _within(path: str, scope: str) -> bool:
    return _safe_relative(path).parts[: len(_safe_relative(scope).parts)] == _safe_relative(scope).parts


def decide(authorization: Authorization | None, request: Request) -> Decision:
    """Return one deterministic decision; malformed authority is indeterminate."""
    try:
        for field in ("actor", "context", "action"):
            _nonempty(getattr(request, field), field)
        if not request.paths:
            raise AuthorityError("request must name at least one bounded path")
        for path in request.paths:
            _safe_relative(path)
    except AuthorityError as exc:
        return Decision(INDETERMINATE, request.action, "none", str(exc), True)
    if authorization is None:
        return Decision(INDETERMINATE, request.action, "none", "explicit authority is missing", True)
    presented = authorization.provenance if isinstance(authorization.provenance, str) else "invalid"
    try:
        for field in ("principal", "context", "provenance"):
            _nonempty(getattr(authorization, field), field)
        if not authorization.allowed_actions or not authorization.allowed_paths:
            raise AuthorityError("allowed actions and scope must be explicit and non-empty")
        for path in authorization.allowed_paths:
            _safe_relative(path)
        if any(not isinstance(action, str) or not action for action in authorization.allowed_actions + authorization.forbidden_actions):
            raise AuthorityError("authority actions must be non-empty strings")
    except (AuthorityError, TypeError) as exc:
        return Decision(INDETERMINATE, request.action, presented, str(exc), True)
    if request.actor != authorization.principal:
        return Decision(DENIED, request.action, presented, "actor is outside the named principal", True)
    if request.context != authorization.context:
        return Decision(DENIED, request.action, presented, "authority context does not match request context", True)
    if request.action in authorization.forbidden_actions:
        return Decision(DENIED, request.action, presented, "action is explicitly forbidden", True)
    if request.action not in authorization.allowed_actions:
        return Decision(DENIED, request.action, presented, "action is not explicitly allowed", True)
    if any(not any(_within(path, scope) for scope in authorization.allowed_paths) for path in request.paths):
        return Decision(DENIED, request.action, presented, "requested path escapes allowed scope", True)
    return Decision(AUTHORIZED, request.action, presented, "explicit bounded authority matches request", False)


class AppendOnlyAudit:
    """Append canonical JSONL decision evidence; existing bytes are never changed."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, request: Request, decision: Decision) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        event = {"decision": asdict(decision), "request": asdict(request), "schema_version": "0.1.0"}
        encoded = json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n"
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())


def guarded_execute(
    authorization: Authorization | None,
    request: Request,
    audit: AppendOnlyAudit,
    effect: Callable[[], _T],
) -> _T:
    """Audit then run an effect only for an AUTHORIZED decision."""
    decision = decide(authorization, request)
    audit.append(request, decision)
    if decision.state != AUTHORIZED:
        raise AuthorityError(json.dumps(asdict(decision), sort_keys=True, separators=(",", ":")))
    return effect()
