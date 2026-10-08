from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ui.theme import (
    PRIMARY, ACCENT, OK, BAD, FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import Screen, KEY_ESC, KEY_ENTER
from utils.paths import APIS_PATH, CONFIG_PATH
from utils.version import (
