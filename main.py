#!/usr/bin/env python3
"""Write the pre-rendered front page to the output directory.

Standard library only. The page is drawn at build time by render.py;
this program copies the entry.png beside it to $MAKEFUN_OUTPUT_DIR
(default /output) as entry.png, and refuses to finish unless the copy
is byte-identical to the source.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    if os.path.getsize(dst) != os.path.getsize(SRC):
        print("copy size mismatch", file=sys.stderr)
        return 1
    if sha256_file(dst) != sha256_file(SRC):
        print("copy hash mismatch", file=sys.stderr)
        return 1
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
