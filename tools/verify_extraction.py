#!/usr/bin/env python3
"""Verify immutable extraction provenance plus declared prospective evolution."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-repository", type=Path, required=True)
    parser.add_argument("--framework", type=Path, default=Path("."))
    args = parser.parse_args()

    extraction = json.loads(
        (args.framework / "provenance/extraction-manifest.json").read_text()
    )
    evolution_path = args.framework / "provenance/evolution-manifest.json"
    evolved = {}
    if evolution_path.is_file():
        evolution = json.loads(evolution_path.read_text())
        evolved = {
            entry["path"]: entry
            for entry in evolution.get("evolved_extracted_surfaces", [])
        }

    try:
        subprocess.check_call(
            [
                "git",
                "-C",
                str(args.source_repository),
                "cat-file",
                "-e",
                f"{extraction['source_commit']}^{{commit}}",
            ]
        )
    except subprocess.CalledProcessError:
        raise SystemExit("FAIL: pinned source commit is unavailable from source repository")

    for entry in extraction["entries"]:
        source_path = entry["source_path"]
        destination = entry["destination_path"]
        blob = subprocess.check_output(
            [
                "git",
                "-C",
                str(args.source_repository),
                "rev-parse",
                f"{extraction['source_commit']}:{source_path}",
            ],
            text=True,
        ).strip()
        if blob != entry["source_git_blob_sha"]:
            raise SystemExit(f"FAIL: source Git blob mismatch {source_path}")
        if sha(args.source_repository / source_path) != entry["content_sha256"]:
            raise SystemExit(f"FAIL: source content mismatch {source_path}")

        current = sha(args.framework / destination)
        if destination in evolved:
            evo = evolved[destination]
            if evo["baseline_sha256"] != entry["content_sha256"]:
                raise SystemExit(f"FAIL: evolution baseline mismatch {destination}")
            if current != evo["candidate_sha256"]:
                raise SystemExit(f"FAIL: evolved candidate mismatch {destination}")
        elif current != entry["content_sha256"]:
            raise SystemExit(f"FAIL: undeclared extraction drift {destination}")

    extra = set(evolved) - {entry["destination_path"] for entry in extraction["entries"]}
    if extra:
        raise SystemExit(f"FAIL: evolution references non-extracted surfaces: {sorted(extra)}")

    print(
        f"PASS: {len(extraction['entries'])} source extractions verified; "
        f"{len(evolved)} prospectively evolved surfaces declared and matched"
    )


if __name__ == "__main__":
    main()
