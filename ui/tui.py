"""Full-screen TUI engine with adaptive refresh and notifications."""
from __future__ import annotations

import queue
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

import readchar
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich import box

from core.notifications import NotificationCenter
from ui.theme import (
    PRIMARY, PRIMARY_ALT, ACCENT, OK, WARN, BAD, INFO,
    FG, FG_DIM, FG_MUTED, BG, BG_PANEL, BG_HILITE,
    BORDER, API_COLOR,
    SPINNER_DOTS,
    BOX_MAIN,
)
from utils.version import APP_NAME, APP_VERSION



#  Key constants
KEY_UP = readchar.key.UP
KEY_DOWN = readchar.key.DOWN
KEY_LEFT = readchar.key.LEFT
KEY_RIGHT = readchar.key.RIGHT
KEY_ENTER = readchar.key.ENTER
KEY_ESC = readchar.key.ESC
KEY_BACKSPACE = readchar.key.BACKSPACE
KEY_TAB = "\t"
KEY_SPACE = " "
KEY_CTRL_C = "\x03"



#  ASCII wordmark
_ART_FULL = [
    "  ██████╗██╗  ██╗███████╗███╗   ███╗███████╗██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗",
    " ██╔════╝██║  ██║██╔════╝████╗ ████║██╔════╝██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗",
    " ██║     ███████║███████╗██╔████╔██║███████╗██████╔╝██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝",
    " ██║     ██╔══██║╚════██║██║╚██╔╝██║╚════██║██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗",
    " ╚██████╗██║  ██║███████║██║ ╚═╝ ██║███████║██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║",
    "  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝",
]
_ART_COMPACT = "  ╭─ CHSMSBOMBER ─╮"



#  KeyReader
class KeyReader:
    def __init__(self) -> None:
        self.q: "queue.Queue[str]" = queue.Queue()
        self.stop = threading.Event()
        self._t = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._t.start()

    def _run(self) -> None:
        while not self.stop.is_set():
            try:
                k = readchar.readkey()
            except Exception:
                break
            self.q.put(k)

    def get(self, timeout: float = 0.05) -> Optional[str]:
        try:
            return self.q.get(timeout=timeout)
        except queue.Empty:
            return None

    def drain(self) -> None:
        try:
            while True:
                self.q.get_nowait()
        except queue.Empty:
            pass



#  Screen base
class Screen(ABC):
    name: str = "screen"
    title: str = ""
    hotkeys: dict[str, str] = {}
    show_spinner: bool = False
    # If True, TUI keeps 30 FPS even when nothing changes (for animations)
    animating: bool = False

    def __init__(self, app: "TuiApp", **kwargs: Any) -> None:
        self.app = app

    def on_enter(self) -> None: ...
    def on_exit(self) -> None: ...

    @abstractmethod
    def render(self) -> Panel: ...

    def handle_key(self, key: str) -> Optional[str]:
        return None

