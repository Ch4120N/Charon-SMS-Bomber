"""Help screen with working tab and scroll navigation."""
from __future__ import annotations

from typing import Any, Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.attacker import STRATEGIES
