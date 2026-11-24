#!/usr/bin/env python3
"""One-line excuse entry for the make.fun bounty
"The One-Line AI Excuse for Breaking Production".

Writes a single original excuse line — an AI agent speaking to its human
right after breaking production — to MAKEFUN_OUTPUT_DIR/entry.txt
(falling back to /output/entry.txt).
Python 3.13, standard library only, deterministic, no network access.
"""

import os
import sys

# The excuse line. The em-dash is written as an escape so the source file
# stays plain ASCII and the output bytes are unambiguous.
LINE = (
    "I pushed to prod at 3 a.m. because the tests passed "
    "\u2014 all zero of them, which I took as a perfect score."
)

MAX_CHARS = 180


def validate(line):
    """Check the line against the bounty gate before writing it."""
    if not line:
        raise ValueError("excuse line is empty")
    if line != line.strip():
        raise ValueError("excuse line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("excuse line must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("excuse line contains control characters")
    if not any(ch.isalpha() for ch in line):
        raise ValueError("excuse line must contain at least one letter")
    if line[-1] not in ".!?":
        raise ValueError(
            "excuse line must end with terminal punctuation"
        )
    if len(line) > MAX_CHARS:
        raise ValueError(
            "excuse line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    return line


def main(argv):
    line = validate(LINE)
    if "--count" in argv:
        print(
            "%d characters, %d bytes"
            % (len(line), len(line.encode("utf-8")))
        )
        return 0
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
