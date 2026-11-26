#!/usr/bin/env python3
"""Entry program for news-image-20261126.

Copies the front-page image this repository ships (entry.png) to the
output directory make.fun provides, so the judge sees exactly the
newspaper front page summing up Thursday 26 November 2026.
Standard library only; no network; deterministic output.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    # The judge reads exactly this file; its name stays entry.png.
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
