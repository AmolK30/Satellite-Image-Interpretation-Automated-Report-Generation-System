from __future__ import annotations

from pathlib import Path
import tempfile

from PIL import Image

from backend.services.classifier import LandCoverClassifier
from backend.services.environmental_analyzer import EnvironmentalAnalyzer
from backend.services.feature_extractor import extract_features, load_image, validate_image_file
from backend.services.pipeline import AnalysisPipeline


def _create_test_image(color: tuple[int, int, int]) -> str:
    temp_dir = Path(tempfile.mkdtemp())
    image_path = temp_dir / "sample.png"
    image = Image.new("RGB", (64, 64), color=color)
    image.save(image_path)
    return str(image_path)


def test_validate_image_file_accepts_supported_extension():
    validate_image_file("scene.png")


def test_classifier_returns_distribution_sum_100():
    image_path = _create_test_image((40, 140, 40))
    image = load_image(image_path)
    features = extract_features(image)
    result = LandCoverClassifier().classify(features)
    assert sum(result.distribution.values()) == 100
    assert result.dominant_class in result.distribution


def test_environment_analyzer_score_range():
    analysis = EnvironmentalAnalyzer().analyze({"agriculture": 40, "forest": 30, "water": 10, "urban": 15, "industrial": 5})
    assert 0 <= analysis.score <= 100


def test_pipeline_analyze_returns_report():
    image_path = _create_test_image((60, 120, 80))
    pipeline = AnalysisPipeline()
    result = pipeline.analyze(image_path=image_path, image_name="sample.png")
    assert "report" in result
    assert "environment_score" in result
    assert sum(result["land_distribution"].values()) == 100
