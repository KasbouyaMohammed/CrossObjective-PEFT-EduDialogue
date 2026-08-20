#!/usr/bin/env python3
"""Rebuild and verify the audited DLDG source archive from GitHub-safe chunks."""
from __future__ import annotations

import argparse
import base64
import hashlib
from pathlib import Path

EXPECTED_SHA256 = "bf3a4392ee4ccfe0839fff6c849791eadfdaace53fac7a09fe223b609b9715f6"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parts-dir", type=Path, default=Path(__file__).parent / "archive_parts")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "dldg_source_code_full.tar.xz")
    args = parser.parse_args()

    parts = sorted(args.parts_dir.glob("part*.b64"))
    expected_names = [f"part{i:02d}.b64" for i in range(1, 7)] + [
        "part07a.b64", "part07b.b64", "part08a.b64", "part08b.b64"
    ]
    names = [p.name for p in parts]
    if names != expected_names:
        raise SystemExit(f"Unexpected chunk set/order: {names}")

    encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
    payload = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"SHA256 mismatch: {digest} != {EXPECTED_SHA256}")

    args.output.write_bytes(payload)
    print(f"Wrote {args.output} ({len(payload):,} bytes)")
    print(f"SHA256 {digest}  OK")


if __name__ == "__main__":
    main()
