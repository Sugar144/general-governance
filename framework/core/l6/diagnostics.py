"""Stable diagnostics shared by governance command-line tools."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, order=True)
class Diagnostic:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message, "path": self.path}


def ordered(items: Iterable[Diagnostic]) -> list[Diagnostic]:
    return sorted(set(items))
