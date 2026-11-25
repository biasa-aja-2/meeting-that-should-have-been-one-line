"""The Meeting That Should Have Been One Line.

Writes a single sentence that could have replaced an entire pointless
meeting to the output directory (MAKEFUN_OUTPUT_DIR, default /output).
Pure stdlib only.
"""

import os
import sys

LINE = "The decision was made before the invite went out; this meeting is just the group photo."


def main():
    # Gate: 1-200 characters, single line, not whitespace-only.
    if not LINE or not LINE.strip():
        print("gate failed: line is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(LINE) > 200:
        print("gate failed: line is %d characters (> 200)" % len(LINE), file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("gate failed: line is not a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read-back verification: exact bytes, valid UTF-8, gate re-checked,
    # and no trailing newline (the entry must be exactly the one line).
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    if text != LINE:
        print("verify failed: read-back does not match", file=sys.stderr)
        return 1
    if text.endswith("\n") or text.endswith("\r"):
        print("verify failed: trailing newline present", file=sys.stderr)
        return 1
    if len(text) != len(LINE) or text.strip() == "" or "\n" in text:
        print("verify failed: gate re-check failed", file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
