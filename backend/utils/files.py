from __future__ import annotations

from pathlib import Path
from uuid import uuid4


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def secure_storage_name(original_name: str) -> str:
    suffix = Path(original_name).suffix.lower()
    return f"{uuid4().hex}{suffix}"
