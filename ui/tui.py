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
