from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.apis import load_apis
from ui.theme import (
    PRIMARY, API_COLOR, API_BRIGHT, OK, WARN, BAD,
    FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import Screen, KEY_UP, KEY_DOWN, KEY_ENTER, KEY_ESC
from ui.widgets import TextInput

