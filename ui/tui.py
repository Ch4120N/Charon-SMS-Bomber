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

        line.append("v" + APP_VERSION, style=HEADER_VERSION)
        line.append("   ")

        crumbs = self.stack
        for i, s in enumerate(crumbs):
            is_last = i == len(crumbs) - 1
            label = s.title or s.name
            if is_last:
                line.append(label, style=f"bold {HEADER_BREADCRUMB_ACTIVE}")
            else:
                line.append(label, style=HEADER_BREADCRUMB)
                line.append("  ›  ", style=HEADER_BREADCRUMB_SEP)

        return Panel(
            Group(Align.left(art), Align.left(line)),
            box=box.ROUNDED,
            border_style=BORDER_DEFAULT,
            padding=(0, 1),
        )

    #  Footer with hotkey chips + notifications
    def _footer(self, screen: Screen) -> Panel:
        from ui.theme import (
            chip, FOOTER_HINT_TEXT, FOOTER_SEPARATOR,
            FOOTER_TOAST_INFO, FOOTER_TOAST_OK, FOOTER_TOAST_WARN,
            FOOTER_TOAST_BAD, FOOTER_TOAST_BULLET, BORDER_DEFAULT,
        )

        hints: list[tuple[str, str]] = [
            ("↑↓", "move"),
            ("⏎", "select"),
        ]
        for k, d in screen.hotkeys.items():
            hints.append((k, d))
        hints.append(("?", "help"))
        hints.append(("Esc", "back"))
        if len(self.stack) <= 1:
            hints.append(("q", "quit"))

        bar = Text()
        for i, (k, d) in enumerate(hints):
            if i > 0:
                bar.append("  ", style=FOOTER_SEPARATOR)
            bar.append_text(Text.from_markup(chip(k)))
            bar.append(f" {d}", style=FOOTER_HINT_TEXT)

        toasts = self.notifications.visible()
        toast_line = Text()
        if toasts:
            toast_line.append(" ")
            for t in toasts:
                toast_line.append("● ", style=FOOTER_TOAST_BULLET)
                # style resolved by toast's own style field
                toast_line.append(t.text, style=t.style)
                toast_line.append("   ")

        body: list[Any] = [Align.left(bar)]
        if toasts:
            body.append(Align.left(toast_line))

        return Panel(
            Group(*body),
