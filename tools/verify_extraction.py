#!/usr/bin/env python3
"""Verify extracted bytes and source Git blobs against immutable source custody."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(); p.add_argument('--source-repository', type=Path, required=True); p.add_argument('--framework', type=Path, default=Path('.')); a=p.parse_args()
    manifest=json.loads((a.framework/'provenance/extraction-manifest.json').read_text())
    try:
        subprocess.check_call(['git','-C',str(a.source_repository),'cat-file','-e',f"{manifest['source_commit']}^{{commit}}"])
    except subprocess.CalledProcessError:
        raise SystemExit('FAIL: pinned source commit is unavailable from source repository')
    for e in manifest['entries']:
        blob=subprocess.check_output(['git','-C',str(a.source_repository),'rev-parse',f"{manifest['source_commit']}:{e['source_path']}"],text=True).strip()
        if blob != e['source_git_blob_sha'] or sha(a.source_repository/e['source_path']) != e['content_sha256'] or sha(a.framework/e['destination_path']) != e['content_sha256']:
            raise SystemExit(f"FAIL: provenance mismatch {e['source_path']}")
    print(f"PASS: {len(manifest['entries'])} extracted files reproduce pinned source blobs and SHA-256")
if __name__ == '__main__': main()
