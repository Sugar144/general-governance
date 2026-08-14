#!/usr/bin/env python3
"""Verify prospective evolution from immutable GOV-GEN extraction provenance."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    extraction = json.loads((ROOT / "provenance/extraction-manifest.json").read_text())
    evolution = json.loads((ROOT / "provenance/evolution-manifest.json").read_text())
    baseline = {
        entry["destination_path"]: entry["content_sha256"]
        for entry in extraction["entries"]
    }
    seen: set[str] = set()
    for entry in evolution["evolved_extracted_surfaces"]:
        path = entry["path"]
        if path in seen:
            fail(f"duplicate evolved surface: {path}")
        seen.add(path)
        if path not in baseline:
            fail(f"evolved surface lacks extraction baseline: {path}")
        if baseline[path] != entry["baseline_sha256"]:
            fail(f"baseline digest mismatch: {path}")
        target = ROOT / path
        if not target.is_file():
            fail(f"evolved surface missing: {path}")
        if sha(target) != entry["candidate_sha256"]:
            fail(f"candidate digest mismatch: {path}")
    print(
        f"PASS: {len(seen)} evolved extracted surfaces preserve baseline provenance "
        "and match prospective candidate bytes"
    )


if __name__ == "__main__":
    main()
