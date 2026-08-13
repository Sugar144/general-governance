"""Atomic publication for new immutable files."""

import os
from pathlib import Path
import tempfile


class ImmutableTargetError(FileExistsError):
    pass


def write_new(path: str | Path, data: bytes) -> None:
    target = Path(path)
    if target.exists() or target.is_symlink():
        raise ImmutableTargetError(f"immutable target already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    temp_path = Path(temporary)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if target.exists() or target.is_symlink():
            raise ImmutableTargetError(f"immutable target already exists: {target}")
        os.replace(temp_path, target)
        directory_fd = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass
