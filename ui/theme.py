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
FOCUS_DIM          = _c("#d47a4e", "color(173)")
FOCUS_BRIGHT       = _c("#ffb88c", "color(216)")
FOCUS_ON_BG        = _c("#0d0e12", "black")

# ══════════════════════════════════════════════════════════════════════
#  5. SEMANTIC
# ══════════════════════════════════════════════════════════════════════

# 5.1 Success — Green
SUCCESS            = _c("#7fd68a", "bright_green")
SUCCESS_DIM        = _c("#5cb068", "green")
SUCCESS_BRIGHT     = _c("#a0e8a8", "bright_green")
SUCCESS_ON_BG      = _c("#0d0e12", "black")

# 5.2 Warning — Yellow
WARNING            = _c("#f0d468", "bright_yellow")
WARNING_DIM        = _c("#c8a848", "yellow")
WARNING_BRIGHT     = _c("#ffe890", "bright_yellow")
WARNING_ON_BG      = _c("#0d0e12", "black")

# 5.3 Error — Red
ERROR              = _c("#e86b6b", "bright_red")
ERROR_DIM          = _c("#c04848", "red")
ERROR_BRIGHT       = _c("#ff8888", "bright_red")
ERROR_ON_BG        = _c("#0d0e12", "black")

# 5.4 Info — Lavender
INFO               = _c("#a4b0f0", "bright_blue")
INFO_DIM           = _c("#7a88c8", "blue")
INFO_BRIGHT        = _c("#c0c8ff", "bright_blue")
INFO_ON_BG         = _c("#0d0e12", "black")

# ══════════════════════════════════════════════════════════════════════
#  6. API / LINK — Cyan (#5fd4e8) — the ONLY cyan family
#     Role: API names in tables, hyperlinks, inline `code` in help
# ══════════════════════════════════════════════════════════════════════
API_NAME           = _c("#5fd4e8", "bright_cyan")
API_NAME_FOCUSED   = _c("#96e8f5", "bright_cyan")
LINK               = _c("#5fd4e8", "bright_cyan")
LINK_UNDERLINE     = LINK
LINK_HOVER         = _c("#96e8f5", "bright_cyan")

# ══════════════════════════════════════════════════════════════════════
#  7. BORDERS
# ══════════════════════════════════════════════════════════════════════
BORDER_DEFAULT     = _c("#2e3342", "grey27")
BORDER_SUBTLE      = _c("#23262f", "grey23")
BORDER_FOCUSED     = BRAND
BORDER_ACCENT      = FOCUS
BORDER_DISABLED    = TEXT_DISABLED
BORDER_STATUS_OK   = SUCCESS_DIM
BORDER_STATUS_WARN = WARNING_DIM
BORDER_STATUS_BAD  = ERROR_DIM

# ══════════════════════════════════════════════════════════════════════
#  8. CHIP BACKGROUNDS — bright, distinct hues for key caps and tabs
# ══════════════════════════════════════════════════════════════════════
CHIP_BG_DEFAULT    = _c("#ffb88c", "color(216)")   # peach orange (key caps)
CHIP_BG_ALT        = _c("#e8a0f5", "bright_magenta")   # magenta (help tabs)
CHIP_BG_OK         = _c("#a0e8a8", "bright_green")     # green
CHIP_BG_WARN       = _c("#ffe890", "bright_yellow")    # yellow
CHIP_BG_BAD        = _c("#ff8888", "bright_red")       # red
CHIP_BG_API        = _c("#96e8f5", "bright_cyan")      # cyan
CHIP_BG_INFO       = _c("#c0c8ff", "bright_blue")      # lavender
CHIP_FG_DEFAULT    = _c("#0d0e12", "black")


# ══════════════════════════════════════════════════════════════════════
#  9. STATUS BAR / FOOTER — every colour used here, defined in-place
#
#     ┌──────────────────────────────────────────────────────────┐
#     │  [↑↓] move   [⏎] select   [?] help   [Esc] back    ● OK  │
#     │   key cap    key cap      key cap    key cap       toast │
#     └──────────────────────────────────────────────────────────┘
# ══════════════════════════════════════════════════════════════════════

# ── 9.1  Panel frame ─────────────────────────────────────────────────
STATUS_BAR_BORDER          = BORDER_DEFAULT        # #2e3342 slate
STATUS_BAR_BG              = SURFACE_BASE          # #0d0e12 app bg

# ── 9.2  Navigation BUTTONS (key caps) ───────────────────────────────
#     Foreground = #0d0e12  (near-black)
#     Background = #ffb88c  (bright peach-orange)
#     Contrast ≈ 14 : 1 — always readable.
STATUS_BAR_KEY_FG          = CHIP_FG_DEFAULT       # #0d0e12
STATUS_BAR_KEY_BG          = CHIP_BG_DEFAULT       # #ffb88c

STATUS_BAR_KEY_FG_FOCUSED  = CHIP_FG_DEFAULT       # #0d0e12
STATUS_BAR_KEY_BG_FOCUSED  = BRAND_BRIGHT          # #f5a0ff

STATUS_BAR_KEY_FG_DISABLED = TEXT_DISABLED         # #454a55
STATUS_BAR_KEY_BG_DISABLED = SURFACE_ELEVATED      # #1e2029

# ── 9.3  Description text next to each key cap ───────────────────────
STATUS_BAR_TEXT            = TEXT_SECONDARY        # #9fa5b2

# ── 9.4  Gap between hotkey groups ───────────────────────────────────
STATUS_BAR_SEPARATOR       = TEXT_DISABLED         # #454a55

# ── 9.5  Toast bullet prefix "●" ─────────────────────────────────────
STATUS_BAR_BULLET          = TEXT_TERTIARY         # #6a7080

# ── 9.6  Toast notification text, per level ──────────────────────────
STATUS_BAR_TOAST_INFO      = INFO                  # #a4b0f0 lavender
STATUS_BAR_TOAST_OK        = SUCCESS               # #7fd68a green
STATUS_BAR_TOAST_WARN      = WARNING               # #f0d468 yellow
STATUS_BAR_TOAST_BAD       = ERROR                 # #e86b6b red


# ══════════════════════════════════════════════════════════════════════
# 10. FOOTER aliases
# ══════════════════════════════════════════════════════════════════════
FOOTER_HINT_TEXT    = STATUS_BAR_TEXT
FOOTER_SEPARATOR    = STATUS_BAR_SEPARATOR
FOOTER_TOAST_INFO   = STATUS_BAR_TOAST_INFO
FOOTER_TOAST_OK     = STATUS_BAR_TOAST_OK
FOOTER_TOAST_WARN   = STATUS_BAR_TOAST_WARN
FOOTER_TOAST_BAD    = STATUS_BAR_TOAST_BAD
FOOTER_TOAST_BULLET = STATUS_BAR_BULLET

# ══════════════════════════════════════════════════════════════════════
# 11. HEADER
# ══════════════════════════════════════════════════════════════════════
HEADER_ART                = BRAND                  # magenta wordmark
HEADER_VERSION            = TEXT_TERTIARY
HEADER_BREADCRUMB         = TEXT_TERTIARY
HEADER_BREADCRUMB_ACTIVE  = BRAND_BRIGHT
HEADER_BREADCRUMB_SEP     = TEXT_DISABLED
HEADER_SPINNER            = SUCCESS
HEADER_SPINNER_IDLE       = TEXT_TERTIARY

# ══════════════════════════════════════════════════════════════════════
# 12. MENUS
# ══════════════════════════════════════════════════════════════════════
MENU_MARKER         = BRAND
MENU_ITEM           = TEXT_PRIMARY
MENU_ITEM_FOCUSED   = BRAND_BRIGHT
MENU_DESC           = TEXT_TERTIARY
MENU_DESC_FOCUSED   = TEXT_SECONDARY
MENU_SEPARATOR      = TEXT_DISABLED
MENU_GROUP_LABEL    = FOCUS                        # orange section header

# ══════════════════════════════════════════════════════════════════════
# 13. FORMS
# ══════════════════════════════════════════════════════════════════════
FORM_LABEL          = TEXT_PRIMARY
FORM_LABEL_FOCUSED  = FOCUS                        # orange
FORM_VALUE          = TEXT_PRIMARY
FORM_VALUE_FOCUSED  = TEXT_PRIMARY
FORM_CURSOR_FG      = TEXT_INVERSE
FORM_CURSOR_BG      = FOCUS
FORM_HINT           = TEXT_TERTIARY
FORM_PLACEHOLDER    = TEXT_DISABLED
FORM_MARKER         = BRAND
FORM_SECTION_LABEL  = FOCUS
FORM_ACTION         = WARNING                      # yellow start-attack
FORM_ACTION_FOCUS   = WARNING_BRIGHT
FORM_ACTION_DIM     = WARNING_DIM

# ══════════════════════════════════════════════════════════════════════
# 14. TOGGLES
# ══════════════════════════════════════════════════════════════════════
TOGGLE_ON_BG        = SUCCESS                      # green
TOGGLE_ON_FG        = TEXT_INVERSE
TOGGLE_OFF_BG       = ERROR_DIM                    # red
TOGGLE_OFF_FG       = TEXT_INVERSE

# ══════════════════════════════════════════════════════════════════════
# 15. CYCLES
# ══════════════════════════════════════════════════════════════════════
CYCLE_BG            = FOCUS_DIM                    # muted orange
CYCLE_FG            = TEXT_INVERSE
CYCLE_FG_FOCUSED    = TEXT_INVERSE
CYCLE_BG_FOCUSED    = FOCUS                        # bright orange
CYCLE_ARROW         = FOCUS_BRIGHT

# ══════════════════════════════════════════════════════════════════════
# 16. TABLES
# ══════════════════════════════════════════════════════════════════════
TABLE_HEADER        = FOCUS                        # orange column titles
TABLE_ROW           = TEXT_PRIMARY
TABLE_ROW_ALT       = TEXT_SECONDARY
TABLE_ROW_FOCUSED   = BRAND_BRIGHT                 # magenta cursor row
TABLE_ROW_DISABLED  = TEXT_DISABLED
TABLE_CELL_BORDER   = BORDER_SUBTLE
TABLE_MARKER        = BRAND
TABLE_TITLE         = BRAND

# ══════════════════════════════════════════════════════════════════════
# 17. PROGRESS
