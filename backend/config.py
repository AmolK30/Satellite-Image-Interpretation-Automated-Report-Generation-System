from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent


@dataclass(frozen=True)
class Config:
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key")
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{PROJECT_ROOT / 'satellite_analysis.db'}")
    upload_folder: str = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    report_folder: str = os.getenv("REPORT_FOLDER", str(BASE_DIR / "reports"))
    max_content_length: int = int(os.getenv("MAX_CONTENT_LENGTH", str(25 * 1024 * 1024)))
    enable_hf_models: bool = os.getenv("ENABLE_HF_MODELS", "false").lower() in {"1", "true", "yes"}
    hf_text_model: str = os.getenv("HF_TEXT_MODEL", "google/flan-t5-base")
