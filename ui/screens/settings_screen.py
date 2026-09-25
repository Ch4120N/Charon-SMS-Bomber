from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.attacker import STRATEGIES
from core.config import save_config
from ui.theme import (
    PRIMARY, ACCENT, OK, WARN, BAD,
    FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import (
    Screen, KEY_UP, KEY_DOWN, KEY_ENTER, KEY_ESC, KEY_SPACE,
    KEY_LEFT, KEY_RIGHT,
)
from ui.widgets import Field


def _build_fields(cfg: dict) -> list[Field]:
    A, N, U, H, O, L = (
