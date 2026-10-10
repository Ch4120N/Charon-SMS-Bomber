"""API registry: load, filter, dedupe, expand."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from utils.paths import APIS_PATH

# Applied to every request unless the API overrides them.
DEFAULT_HEADERS: dict[str, str] = {
