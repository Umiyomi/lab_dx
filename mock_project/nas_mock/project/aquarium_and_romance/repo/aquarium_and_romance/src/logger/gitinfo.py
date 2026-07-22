"""Git state helpers for run metadata."""

from __future__ import annotations

import subprocess
from typing import Any

from src.config import ROOT


def _run_git(*args: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def capture_git_state() -> dict[str, Any]:
    commit = _run_git("rev-parse", "HEAD")
    branch = _run_git("rev-parse", "--abbrev-ref", "HEAD")
    status = _run_git("status", "--porcelain")
    dirty = bool(status) if status is not None else None

    return {
        "commit": commit[:7] if commit else None,
        "branch": branch,
        "dirty": dirty,
    }
