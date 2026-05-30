from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import logging

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError


LOGGER = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}


@dataclass(frozen=True)
class ImageFeatures:
    width: int
    height: int
    mean_rgb: list[float]
    std_rgb: list[float]
    vegetation_index: float
    water_index: float
    urban_index: float
    barren_index: float
    texture_score: float
    edge_score: float


def validate_image_file(filename: str, file_size: int | None = None, max_size: int | None = None) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported file format. Allowed: JPG, PNG, TIFF, GeoTIFF, BMP, WEBP.")
    if file_size is not None and max_size is not None and file_size > max_size:
        raise ValueError("File size exceeds the configured limit.")


def load_image(image_path: str | Path) -> Image.Image:
    try:
        image = Image.open(image_path)
        image = ImageOps.exif_transpose(image)
        return image.convert("RGB")
    except UnidentifiedImageError as exc:
        raise ValueError("Unable to read image file. The file may be corrupted.") from exc


def preprocess_image(image: Image.Image, target_size: tuple[int, int] = (224, 224)) -> np.ndarray:
    resized = image.resize(target_size)
    return np.asarray(resized, dtype=np.float32) / 255.0


def extract_features(image: Image.Image) -> ImageFeatures:
    array = preprocess_image(image)
    width, height = image.size
    mean_rgb = array.mean(axis=(0, 1)).tolist()
    std_rgb = array.std(axis=(0, 1)).tolist()

    red = array[:, :, 0]
    green = array[:, :, 1]
    blue = array[:, :, 2]

    vegetation_index = float(np.clip((green.mean() - red.mean()) + green.std() * 0.2, 0.0, 1.0))
    water_index = float(np.clip((blue.mean() - green.mean() * 0.25) + (1.0 - array.mean(axis=2)).mean() * 0.2, 0.0, 1.0))
    urban_index = float(np.clip((array.mean(axis=2) < 0.45).mean() * 0.7 + np.abs(red - green).mean() * 0.3, 0.0, 1.0))
    barren_index = float(np.clip((red.mean() * 0.5 + green.mean() * 0.25 - blue.mean() * 0.1), 0.0, 1.0))

    grayscale = array.mean(axis=2)
    gx = np.abs(np.diff(grayscale, axis=1)).mean() if grayscale.shape[1] > 1 else 0.0
    gy = np.abs(np.diff(grayscale, axis=0)).mean() if grayscale.shape[0] > 1 else 0.0
    edge_score = float(np.clip((gx + gy) * 1.8, 0.0, 1.0))
    texture_score = float(np.clip(grayscale.std() * 1.8 + edge_score * 0.4, 0.0, 1.0))

    return ImageFeatures(
        width=width,
        height=height,
        mean_rgb=[float(value) for value in mean_rgb],
        std_rgb=[float(value) for value in std_rgb],
        vegetation_index=vegetation_index,
        water_index=water_index,
        urban_index=urban_index,
        barren_index=barren_index,
        texture_score=texture_score,
        edge_score=edge_score,
    )


def to_dict(features: ImageFeatures) -> dict[str, Any]:
    return {
        "width": features.width,
        "height": features.height,
        "mean_rgb": features.mean_rgb,
        "std_rgb": features.std_rgb,
        "vegetation_index": features.vegetation_index,
        "water_index": features.water_index,
        "urban_index": features.urban_index,
        "barren_index": features.barren_index,
        "texture_score": features.texture_score,
        "edge_score": features.edge_score,
    }
