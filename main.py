#!/usr/bin/env python3
"""A house cat leaves a one-star review of its human.

The cat's complaint is about sleeping arrangements: the human bought
a perfectly good bed and then parked it in the one corner of the
house where the sun never lands, so the cat has moved onto the
laptop instead. The laptop objects loudly. The cat does not care,
and considers the noise part of the bed's charm.

The program itself is deliberately boring. It holds one fixed review,
checks it against the bounty's gate (a single line, 1 to 200
characters, not blank, no stray whitespace at either end), writes it
to entry.txt with no trailing newline, then reads the file back and
refuses to report success unless the bytes on disk are exactly the
review it meant to write. Only the standard library is used, and
there is no clock, no randomness and no network, so every run writes
the same file.
"""

import os
import sys

REVIEW = (
    "One star. He bought me a bed, then put it where the sun never "
    "lands. I sleep on his laptop now. It screams when I sit."
)

ENTRY_FILENAME = "entry.txt"

LOWEST_ALLOWED = 1
HIGHEST_ALLOWED = 200


def check_review(text):
    """Return why the review fails the gate, or "" when it passes."""
    if len(text) < LOWEST_ALLOWED:
        return "review is empty"
    if len(text) > HIGHEST_ALLOWED:
        return "review is %d characters, over the 200 limit" % len(text)
    if text.strip() == "":
        return "review is only whitespace"
    if text != text.strip():
        return "review has leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return "review must be a single line"
    return ""


def target_folder():
    """Pick the output folder: $MAKEFUN_OUTPUT_DIR, else /output."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if wanted:
        return wanted
    return "/output"


def run():
    fault = check_review(REVIEW)
    if fault:
        print("refusing to write entry: %s" % fault, file=sys.stderr)
        return 1
    folder = target_folder()
    os.makedirs(folder, exist_ok=True)
    destination = os.path.join(folder, ENTRY_FILENAME)
    with open(destination, "w", encoding="utf-8", newline="") as out:
        out.write(REVIEW)
    with open(destination, "rb") as out:
        stored = out.read()
    if stored != REVIEW.encode("utf-8"):
        print("entry.txt on disk does not match the review", file=sys.stderr)
        return 1
    print("wrote %s (%d characters)" % (destination, len(REVIEW)))
    return 0


if __name__ == "__main__":
    sys.exit(run())
