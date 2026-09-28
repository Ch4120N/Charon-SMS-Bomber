"""HTTP sender with retries, proxies, and response-body verification."""
from __future__ import annotations

import json
import random
import re
import time
from typing import Any, Optional

import requests
from fake_useragent import UserAgent


