"""Phone number normalization and parsing."""
from __future__ import annotations

from typing import Optional


def normalize_phone(raw: str) -> Optional[str]:
    """Return +98XXXXXXXXXX or None if invalid."""
    s = raw.strip().replace(" ", "").replace("-", "")
    if not s:
        return None
    if s.startswith("+98"):
        pass
    elif s.startswith("98") and len(s) >= 12:
        s = "+" + s
    elif s.startswith("0") and len(s) == 11:
        s = "+98" + s[1:]
    else:
        return None
    if len(s) != 13 or not s[1:].isdigit():
        return None
    return s


def parse_targets(raw: str) -> list[str]:
    """Split by ';' or ',', normalize, dedupe, preserve order."""
    out: list[str] = []
    seen: set[str] = set()
    for token in raw.replace(",", ";").split(";"):
        n = normalize_phone(token)
        if n and n not in seen:
            seen.add(n)
