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
