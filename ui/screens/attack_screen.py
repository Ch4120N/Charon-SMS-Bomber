from __future__ import annotations

import threading
from pathlib import Path
from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.attacker import Attacker, STRATEGIES
from core.history import append_history, make_entry
from core.session import save_session
from core.stats import export_csv, export_html, export_json
from ui.theme import (
    PRIMARY, PRIMARY_ALT, API_COLOR, ACCENT, OK, WARN, BAD,
    FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN, SPINNER_BAR,
)
from ui.tui import Screen, KEY_ESC, KEY_ENTER, KEY_SPACE
from utils.paths import REPORTS_DIR
from utils.version import NOTICE


class AttackScreen(Screen):
    name = "attack"
    title = "Attack"
    hotkeys = {"space": "stop", "Esc": "stop/back", "s": "save reports"}
    show_spinner = True
