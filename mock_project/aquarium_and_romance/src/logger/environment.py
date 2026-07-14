"""Execution environment capture."""

from __future__ import annotations

import hashlib
import platform
import sys
from typing import Any

from src.config import UV_LOCK


def capture_environment() -> dict[str, Any]:
    env: dict[str, Any] = {
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "python_implementation": platform.python_implementation(),
        "package_manager": "uv",
    }
    if UV_LOCK.exists():
        digest = hashlib.sha256(UV_LOCK.read_bytes()).hexdigest()[:12]
        env["lockfile"] = {
            "path": "uv.lock",
            "sha256_12": digest,
        }
    else:
        env["lockfile"] = None
    return env
