from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.attacker import STRATEGIES
from core.phone import parse_targets
from core.session import load_session
from ui.theme import (
    PRIMARY, PRIMARY_ALT, ACCENT, OK, WARN, BAD,
    FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
