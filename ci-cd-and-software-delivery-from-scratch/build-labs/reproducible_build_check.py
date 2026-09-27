#!/usr/bin/env python3
"""
Reproducible Build Validator (Phase 48)
Demonstrates:
- Bit-for-bit reproducibility
- Why timestamps, file ordering, and user IDs cause non-deterministic artifact hashes
- How to enforce determinism with SOURCE_DATE_EPOCH and sorted tar entries
"""

import hashlib
import io
import os
import sys
import tarfile
import time


def build_naive_archive(content: str) -> bytes:
    """Naive build: uses current wall-clock timestamp and default tar ordering."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        data = content.encode("utf-8")
        ti = tarfile.TarInfo(name="app.py")
        ti.size = len(data)
        ti.mtime = time.time()  # Non-deterministic!
        tar.addfile(ti, io.BytesIO(data))
    return buf.getvalue()


import gzip

def build_reproducible_archive(content: str, epoch: int = 1700000000) -> bytes:
    """Reproducible build: fixed mtime (SOURCE_DATE_EPOCH), zeroed UID/GID, normalized gzip header."""
    raw_tar = io.BytesIO()
    with tarfile.open(fileobj=raw_tar, mode="w:") as tar:
        data = content.encode("utf-8")
        ti = tarfile.TarInfo(name="app.py")
        ti.size = len(data)
        ti.mtime = epoch
        ti.uid = 0
        ti.gid = 0
        ti.uname = ""
        ti.gname = ""
        tar.addfile(ti, io.BytesIO(data))
    
    # Compress with fixed timestamp in gzip header
    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, mtime=epoch) as gz:
        gz.write(raw_tar.getvalue())
    return compressed.getvalue()


def main():
    print("=== REPRODUCIBLE BUILD EXPERIMENT (Phase 48) ===")
    source_code = "print('Hello from production service')\n"

    print("\n1. Testing Naive Builds (Different build times):")
    build_1 = build_naive_archive(source_code)
    time.sleep(1.05)  # Advance time so mtime changes
    build_2 = build_naive_archive(source_code)

    hash_1 = hashlib.sha256(build_1).hexdigest()
    hash_2 = hashlib.sha256(build_2).hexdigest()

    print(f"  Build 1 SHA-256: {hash_1}")
    print(f"  Build 2 SHA-256: {hash_2}")
    if hash_1 != hash_2:
        print("  ✗ FAILURE: Artifacts are NON-REPRODUCIBLE despite identical source!")
        print("    Root Cause: Wall-clock filesystem modification timestamps embedded in tar/gzip header.")

    print("\n2. Testing Hermetic Reproducible Builds (SOURCE_DATE_EPOCH enforced):")
    fixed_epoch = 1727400000
    rep_1 = build_reproducible_archive(source_code, epoch=fixed_epoch)
    time.sleep(1.05)
    rep_2 = build_reproducible_archive(source_code, epoch=fixed_epoch)

    rep_hash_1 = hashlib.sha256(rep_1).hexdigest()
    rep_hash_2 = hashlib.sha256(rep_2).hexdigest()

    print(f"  Reproducible Build 1 SHA-256: {rep_hash_1}")
    print(f"  Reproducible Build 2 SHA-256: {rep_hash_2}")

    if rep_hash_1 == rep_hash_2:
        print("  ✓ SUCCESS: Bit-for-bit identical hashes achieved across separate builds!")
    else:
        print("  ✗ FAILURE: Hashes do not match.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
