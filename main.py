#!/usr/bin/env python3
"""Entry program for news-image-20261121.

Copies the pre-rendered front page (entry.png, sitting next to this
file) into the output directory the grader provides.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        raise SystemExit("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # copyfile keeps the bytes identical on every run: no re-encode.
    shutil.copyfile(SOURCE, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
