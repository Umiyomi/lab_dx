"""ResearchRun: record inputs, outputs, git state, and environment for one execution."""

from __future__ import annotations

import getpass
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from src.config import ROOT, RUNS_DIR
from src.logger.environment import capture_environment
from src.logger.gitinfo import capture_git_state


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _generate_run_id(runs_dir: Path) -> str:
    today = datetime.now().strftime("%Y%m%d")
    existing = sorted(runs_dir.glob(f"{today}_*.yaml"))
    next_n = 1
    if existing:
        suffixes = []
        for path in existing:
            parts = path.stem.split("_", 1)
            if len(parts) == 2 and parts[1].isdigit():
                suffixes.append(int(parts[1]))
        if suffixes:
            next_n = max(suffixes) + 1
    return f"{today}_{next_n:03d}"


def _resolve_path(path: str | Path) -> Path:
    resolved = Path(path)
    if not resolved.is_absolute():
        resolved = ROOT / resolved
    return resolved


def _to_rel(path: Path) -> str | None:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return None


def _path_fields(path: Path) -> dict[str, str | None]:
    resolved = path.resolve()
    return {
        "path": _to_rel(resolved),
        "path_abs": resolved.as_posix(),
    }


def _describe_asset(path: Path) -> dict[str, Any]:
    resolved = path.resolve()
    record: dict[str, Any] = _path_fields(resolved)
    if not resolved.exists():
        record["exists"] = False
        return record

    stat = resolved.stat()
    digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
    record.update(
        {
            "exists": True,
            "size": stat.st_size,
            "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            "sha256": digest,
        }
    )
    return record


def _snapshot_dir(root: Path) -> dict[str, dict[str, int | float]]:
    """Map absolute path string -> {size, mtime} for files under root."""
    snapshot: dict[str, dict[str, int | float]] = {}
    if not root.exists():
        return snapshot
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        resolved = path.resolve()
        snapshot[str(resolved)] = {
            "size": resolved.stat().st_size,
            "mtime": resolved.stat().st_mtime,
        }
    return snapshot


def _diff_and_describe(
    before: dict[str, dict[str, int | float]],
    after: dict[str, dict[str, int | float]],
) -> dict[str, list[Any]]:
    before_keys = set(before)
    after_keys = set(after)
    created_paths = sorted(after_keys - before_keys)
    deleted_paths = sorted(before_keys - after_keys)
    modified_paths = sorted(
        key
        for key in before_keys & after_keys
        if before[key]["size"] != after[key]["size"] or before[key]["mtime"] != after[key]["mtime"]
    )
    return {
        "created": [_describe_asset(Path(p)) for p in created_paths],
        "modified": [_describe_asset(Path(p)) for p in modified_paths],
        "deleted": [{**_path_fields(Path(p)), "exists": False} for p in deleted_paths],
    }


class ResearchRun:
    """Context manager that logs one research pipeline execution."""

    def __init__(self, entrypoint: str = "main.py") -> None:
        self.entrypoint = entrypoint
        self.run_id: str | None = None
        self.user = getpass.getuser()
        self.started_at: str | None = None
        self.ended_at: str | None = None
        self._inputs: list[dict[str, Any]] = []
        self._output_roots: list[Path] = []
        self._output_before: dict[Path, dict[str, dict[str, int | float]]] = {}
        self._metadata_path: Path | None = None

    def input(self, path: str | Path) -> Path:
        """Declare an input data asset used by this run."""
        resolved = _resolve_path(path)
        self._inputs.append(_describe_asset(resolved))
        return resolved

    def output(self, root: str | Path) -> Path:
        """Declare an output root directory. Files under it are detected by snapshot diff."""
        resolved = _resolve_path(root)
        resolved.mkdir(parents=True, exist_ok=True)
        self._output_roots.append(resolved)
        self._output_before[resolved] = _snapshot_dir(resolved)
        return resolved

    def __enter__(self) -> ResearchRun:
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        self.run_id = _generate_run_id(RUNS_DIR)
        self.started_at = _now_iso()
        self._metadata_path = RUNS_DIR / f"{self.run_id}.yaml"
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.ended_at = _now_iso()
        outputs: list[dict[str, Any]] = []
        for root in self._output_roots:
            before = self._output_before.get(root, {})
            after = _snapshot_dir(root)
            record = {
                "root": _to_rel(root),
                "root_abs": root.resolve().as_posix(),
            }
            record.update(_diff_and_describe(before, after))
            outputs.append(record)

        payload = {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "status": "failed" if exc_type else "ok",
            "entrypoint": self.entrypoint,
            "user": self.user,
            "git": capture_git_state(),
            "inputs": self._inputs,
            "outputs": outputs,
            "environment": capture_environment(),
        }
        if self._metadata_path is not None:
            self._metadata_path.write_text(
                yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
            print(f"Run metadata: {_path_fields(self._metadata_path)['path']}")
        return None
