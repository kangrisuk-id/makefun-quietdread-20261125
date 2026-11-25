"""Two Days of Quiet Dread — entry program (program/v1).

Writes one code-review comment to $MAKEFUN_OUTPUT_DIR/entry.txt:
a single line of at most 140 characters that approves a pull request
while carrying quiet existential dread. Pure Python standard library.
"""

import os
import sys

# Winner of the 40-candidate knockout tournament (candidates.md):
# C3, 82 characters, tournament score 24/25 — "Ship it" approves,
# the grandchildren image carries the dread, flat to the last word.
ENTRY = "Ship it. My grandchildren will maintain this code. I have made my peace with that."


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Exact bytes, no trailing newline: the gate counts 1-140 characters.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    os.chmod(path, 0o644)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
