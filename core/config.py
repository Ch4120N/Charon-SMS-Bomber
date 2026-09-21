"""Config load / save / merge / migrate."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from utils.paths import CONFIG_PATH
from utils.version import APP_VERSION
