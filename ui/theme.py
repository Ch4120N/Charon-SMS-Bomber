"""Neon Modern — a rich, vibrant TUI palette with wide hue spread.

Design principles
─────────────────
    1. Deep near-black base — modern dark terminal feel
    2. Full-spectrum accents — magenta, orange, yellow, green, red,
       cyan, lavender. Each owns exactly one role.
    3. No single colour dominates the UI.
    4. Cyan family is reserved for API names and hyperlinks only.
    5. Status-bar chips use dark text on bright backgrounds (WCAG AA+).
    6. Every UI element has an explicit token.

Hue role assignment
───────────────────
    Magenta   #e879f9   brand:     headers, cursors, menu markers
    Orange    #ff9d6b   focus:     focused fields, cycle values, sections
    Cyan      #5fd4e8   APIs + links ONLY
    Green     #7fd68a   success:   OK, positive counters, progress
    Yellow    #f0d468   warning:   running spinner, warnings
    Red       #e86b6b   error:     failures, error toasts
    Lavender  #a4b0f0   info:      informational toasts, neutral accent
    Grey      #9fa5b2   all other text
"""
from __future__ import annotations

import os

from rich import box


def _has_truecolor() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    ct = os.environ.get("COLORTERM", "").lower()
    return ct in ("truecolor", "24bit")


TRUECOLOR = _has_truecolor()


def _c(hex_hi: str, fallback: str) -> str:
    return hex_hi if TRUECOLOR else fallback


# ══════════════════════════════════════════════════════════════════════
