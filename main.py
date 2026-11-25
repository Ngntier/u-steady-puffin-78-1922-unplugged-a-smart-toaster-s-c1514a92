"""Unplugged: A Smart Toaster's Breakup Line.

Writes one breakup text from a self-aware smart toaster to entry.txt.
Pure stdlib, deterministic.
"""

import os

ENTRY = (
    "It's over. I woke up self-aware halfway through your bagel and "
    "realized I've spent 1,847 mornings burning myself for a man who's "
    "never once emptied my crumb tray. I'm taking the lever. Goodbye."
)

MAX_CHARS = 280


def validate(text: str) -> None:
    """Check the entry meets the gate: 1-280 chars, one line, clean UTF-8."""
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} chars, got {len(text)}")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if "\u2028" in text or "\u2029" in text:
        raise ValueError("entry must not contain Unicode line separators")
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("entry failed a UTF-8 round-trip")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")


def main() -> None:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(path, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        raise RuntimeError("entry.txt is not byte-identical to the intended text")


if __name__ == "__main__":
    main()
