from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ui.theme import (
    PRIMARY, PRIMARY_ALT, ACCENT, OK, FG, FG_DIM, FG_MUTED,
    BORDER, BOX_MAIN,
)
from ui.tui import Screen, KEY_UP, KEY_DOWN, KEY_ENTER
from utils.version import NOTICE


_ITEMS = [
    ("start",    "Start Attack",       "launch a new SMS attack"),
    ("continue", "Resume Session",     "reuse last saved session"),
    ("settings", "Settings",           "edit config.json values"),
    ("apis",     "API Manager",        "browse, filter, reload APIs"),
    ("updates",  "Check for Updates",  "download latest apis.json"),
    ("logs",     "Live Logs",          "tail the runtime log file"),
    ("history",  "Session History",    "past attack results"),
    ("help",     "Help",               "strategies, hotkeys, concepts"),
    ("about",    "About",              "program info and credits"),
    ("exit",     "Exit",               "quit ChSMSBomber"),
]


class MainMenuScreen(Screen):
