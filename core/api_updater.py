"""Remote API registry updater — checks GitHub for a newer apis.json."""
from __future__ import annotations

import hashlib
import json
import shutil
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

