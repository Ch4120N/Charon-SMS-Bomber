"""Phone number normalization and parsing."""
from __future__ import annotations

from typing import Optional


def normalize_phone(raw: str) -> Optional[str]:
    """Return +98XXXXXXXXXX or None if invalid."""
    s = raw.strip().replace(" ", "").replace("-", "")
