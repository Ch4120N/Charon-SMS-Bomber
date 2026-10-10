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

    def render_cache_key(self) -> Any:
        """Override to enable dirty-flag caching of rendered panels."""
        return None



#  TuiApp
class TuiApp:
    def __init__(
        self,
        console: Console,
        cfg: dict[str, Any],
        apis: list[dict[str, Any]],
        logger: Any,
    ) -> None:
        self.console = console
        self.cfg = cfg
        self.apis = apis
        self.logger = logger
        self.notifications = NotificationCenter()

        self.stack: list[Screen] = []
        self.running = True
        self._screens: dict[str, type[Screen]] = {}
        self._lock = threading.Lock()
        self.frame = 0

        # adaptive refresh
        self._active_fps = int(cfg["ui"]["refresh_per_second"])
        self._idle_fps = int(cfg["ui"].get("idle_refresh_per_second", 4))
        self._last_input_ts = time.time()
        self._idle_after = float(cfg["ui"].get("idle_after_seconds", 1.5))

        # dirty flag cache
        self._cached_layout: Any = None
        self._cached_key: Any = None

        self.keys = KeyReader()
        self.keys.start()

        self._toast_lock = threading.Lock()

    #  API surface for screens
    def register(self, cls: type[Screen]) -> None:
        self._screens[cls.name] = cls

    def push(self, name: str, **kwargs: Any) -> None:
        cls = self._screens[name]
        screen = cls(self, **kwargs)
        self.stack.append(screen)
        screen.on_enter()
        self.invalidate()

    def pop(self) -> None:
        if self.stack:
            top = self.stack.pop()
            top.on_exit()
            self.invalidate()

    def invalidate(self) -> None:
        self._cached_layout = None
        self._cached_key = None

    def notify(self, text: str, style: str = "white", ttl: float = 3.5) -> None:
        self.notifications.push(text, style, ttl)

    #  Header
    def _header(self, screen: Screen) -> Panel:
        from ui.theme import (
            HEADER_ART, HEADER_VERSION, HEADER_BREADCRUMB,
            HEADER_BREADCRUMB_ACTIVE, HEADER_BREADCRUMB_SEP,
            HEADER_SPINNER, HEADER_SPINNER_IDLE,
            BORDER_DEFAULT,
        )

        width = self.console.width
        use_full = width >= 118

        if use_full:
            art = Text()
            for i, line in enumerate(_ART_FULL):
                art.append(line, style=f"bold {HEADER_ART}")
                if i < len(_ART_FULL) - 1:
                    art.append("\n")
        else:
            art = Text(_ART_COMPACT, style=f"bold {HEADER_ART}")

        line = Text(" ")
        if screen.show_spinner:
            frame = SPINNER_DOTS[self.frame % len(SPINNER_DOTS)]
            line.append(frame, style=f"bold {HEADER_SPINNER}")
            line.append("  ")
        else:
            line.append("·", style=HEADER_SPINNER_IDLE)
            line.append("  ")

