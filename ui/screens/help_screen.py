"""Help screen with working tab and scroll navigation."""
from __future__ import annotations

from typing import Any, Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.attacker import STRATEGIES
from ui.theme import (
    PRIMARY, PRIMARY_ALT, API_COLOR, ACCENT, OK, WARN, BAD,
    FG, FG_DIM, FG_MUTED, BORDER,
    BOX_MAIN,
)
from ui.tui import (
    Screen,
    KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT,
    KEY_ESC, KEY_ENTER, KEY_BACKSPACE,
)
from ui.widgets import TextInput


_SECTIONS = ["strategies", "concepts", "hotkeys", "config", "apis"]


