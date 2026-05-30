from __future__ import annotations

"""Copy sample images into the upload folder for quick demos.

This loader is intentionally simple: point it at a directory of JPG/PNG/TIFF
scene samples and it will normalize them into the backend upload store.
"""

from pathlib import Path
import shutil
import sys

from backend.utils.files import ensure_directory, secure_storage_name


def load_samples(source_dir: str, target_dir: str) -> int:
    source = Path(source_dir)
    target = ensure_directory(target_dir)
    copied = 0
    for file_path in source.glob("*"):
        if file_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}:
            continue
        shutil.copy2(file_path, target / secure_storage_name(file_path.name))
        copied += 1
    return copied


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python -m backend.scripts.load_sample_dataset <source_dir> <target_dir>")
    count = load_samples(sys.argv[1], sys.argv[2])
    print(f"Copied {count} files.")
