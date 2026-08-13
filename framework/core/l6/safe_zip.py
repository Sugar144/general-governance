"""Bounded, non-extracting ZIP inspection."""

from dataclasses import dataclass
from pathlib import PurePosixPath, Path
import stat
import zipfile

from .diagnostics import Diagnostic, ordered


MAX_MEMBERS = 128
MAX_MEMBER_BYTES = 8 * 1024 * 1024
MAX_TOTAL_BYTES = 64 * 1024 * 1024
MAX_COMPRESSION_RATIO = 200


@dataclass(frozen=True)
class ZipLimits:
    max_members: int = MAX_MEMBERS
    max_member_bytes: int = MAX_MEMBER_BYTES
    max_total_bytes: int = MAX_TOTAL_BYTES
    max_compression_ratio: int = MAX_COMPRESSION_RATIO


def normalize_member(name: str) -> str:
    if not name or "\\" in name:
        raise ValueError("empty or ambiguous backslash path")
    path = PurePosixPath(name)
    if path.is_absolute() or name.startswith("/"):
        raise ValueError("absolute path")
    if any(part in ("", ".", "..") for part in path.parts):
        raise ValueError("unsafe path segment")
    normalized = path.as_posix()
    if normalized != name.rstrip("/"):
        raise ValueError("non-canonical member path")
    return normalized


def inspect(path: str | Path, limits: ZipLimits = ZipLimits()) -> tuple[dict[str, bytes], list[Diagnostic]]:
    members: dict[str, bytes] = {}
    diagnostics: list[Diagnostic] = []
    total = 0
    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        return {}, [Diagnostic("ZIP_UNREADABLE", "$", str(exc))]
    with archive:
        infos = archive.infolist()
        if len(infos) > limits.max_members:
            diagnostics.append(Diagnostic("ZIP_MEMBER_LIMIT", "$", f"{len(infos)} exceeds {limits.max_members}"))
        seen: set[str] = set()
        for index, info in enumerate(infos):
            label = f"$[{index}]"
            try:
                normalized = normalize_member(info.filename)
            except ValueError as exc:
                diagnostics.append(Diagnostic("ZIP_UNSAFE_PATH", label, f"{info.filename!r}: {exc}"))
                continue
            if normalized in seen:
                diagnostics.append(Diagnostic("ZIP_DUPLICATE_MEMBER", label, normalized))
                continue
            seen.add(normalized)
            mode = (info.external_attr >> 16) & 0xFFFF
            kind = stat.S_IFMT(mode)
            if kind not in (0, stat.S_IFREG):
                diagnostics.append(Diagnostic("ZIP_UNSAFE_FILE_TYPE", label, normalized))
                continue
            if info.is_dir():
                diagnostics.append(Diagnostic("ZIP_DIRECTORY_ENTRY", label, normalized))
                continue
            if info.flag_bits & 0x1:
                diagnostics.append(Diagnostic("ZIP_ENCRYPTED", label, normalized))
                continue
            total += info.file_size
            if info.file_size > limits.max_member_bytes:
                diagnostics.append(Diagnostic("ZIP_MEMBER_SIZE_LIMIT", label, normalized))
                continue
            if total > limits.max_total_bytes:
                diagnostics.append(Diagnostic("ZIP_TOTAL_SIZE_LIMIT", "$", str(total)))
                continue
            ratio = info.file_size / max(info.compress_size, 1)
            if ratio > limits.max_compression_ratio:
                diagnostics.append(Diagnostic("ZIP_COMPRESSION_RATIO_LIMIT", label, normalized))
                continue
            try:
                data = archive.read(info)
            except (OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError) as exc:
                diagnostics.append(Diagnostic("ZIP_MEMBER_UNREADABLE", label, f"{normalized}: {exc}"))
                continue
            if len(data) != info.file_size:
                diagnostics.append(Diagnostic("ZIP_SIZE_MISMATCH", label, normalized))
                continue
            members[normalized] = data
    return members, ordered(diagnostics)
