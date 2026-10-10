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
#  1. SURFACES
# ══════════════════════════════════════════════════════════════════════
SURFACE_BASE       = _c("#0d0e12", "black")
SURFACE_PANEL      = _c("#16171e", "grey11")
SURFACE_ELEVATED   = _c("#1e2029", "grey15")
SURFACE_HOVER      = _c("#272a36", "grey19")
SURFACE_SELECTED   = _c("#333747", "grey23")
SURFACE_INPUT      = _c("#12131a", "grey7")
SURFACE_INPUT_FOC  = _c("#1a1c25", "grey11")

# ══════════════════════════════════════════════════════════════════════
#  2. TEXT
# ══════════════════════════════════════════════════════════════════════
TEXT_PRIMARY       = _c("#e4e6eb", "white")
TEXT_SECONDARY     = _c("#9fa5b2", "grey70")
TEXT_TERTIARY      = _c("#6a7080", "grey54")
TEXT_DISABLED      = _c("#454a55", "grey35")
TEXT_INVERSE       = _c("#0d0e12", "black")

# ══════════════════════════════════════════════════════════════════════
#  3. BRAND — Magenta (#e879f9)
#     Role: header art, breadcrumb active, menu markers, table cursors,
#           focused borders, scrollbar thumb
# ══════════════════════════════════════════════════════════════════════
BRAND              = _c("#e879f9", "bright_magenta")
BRAND_DIM          = _c("#b85cc8", "magenta")
BRAND_BRIGHT       = _c("#f5a0ff", "bright_magenta")
BRAND_ON_BG        = _c("#0d0e12", "black")

# ══════════════════════════════════════════════════════════════════════
#  4. FOCUS — Orange (#ff9d6b)
#     Role: focused field labels, cycle pickers, section titles,
#           form cursor background, tab highlights
# ══════════════════════════════════════════════════════════════════════
FOCUS              = _c("#ff9d6b", "color(215)")
