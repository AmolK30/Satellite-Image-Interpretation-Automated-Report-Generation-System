from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.services.classifier import LandCoverClassifier
from backend.services.disaster_detector import DisasterDetector
from backend.services.environmental_analyzer import EnvironmentalAnalyzer
from backend.services.feature_extractor import extract_features, load_image, to_dict
from backend.services.pdf_exporter import PDFExporter
from backend.services.report_generator import ReportGenerator


class AnalysisPipeline:
    def __init__(self) -> None:
        self.classifier = LandCoverClassifier()
        self.environmental_analyzer = EnvironmentalAnalyzer()
        self.disaster_detector = DisasterDetector()
        self.report_generator = ReportGenerator()
        self.pdf_exporter = PDFExporter()

    def analyze(self, image_path: str | Path, image_name: str, comparison: dict[str, Any] | None = None) -> dict[str, Any]:
        image = load_image(image_path)
        features = extract_features(image)
        classification = self.classifier.classify(features)
        environmental = self.environmental_analyzer.analyze(classification.distribution)
        disaster = self.disaster_detector.assess(classification.distribution, environmental.score)
        report_bundle = self.report_generator.generate(
            image_name=image_name,
            classification=classification,
            environmental=environmental,
            disaster=disaster,
            comparison=comparison,
        )

        return {
            "features": to_dict(features),
            "environment_score": environmental.score,
            "land_distribution": classification.distribution,
            "classification": {
                "confidence": classification.confidence,
                "dominant_class": classification.dominant_class,
                "raw_scores": classification.raw_scores,
            },
            "environmental_summary": {
                "score": environmental.score,
                "interpretation": environmental.interpretation,
                "factors": environmental.factors,
            },
            "disaster_summary": {
                "risk_level": disaster.risk_level,
                "threats": disaster.threats,
                "recommendations": disaster.recommendations,
            },
            "report": report_bundle.report_text,
            "executive_summary": report_bundle.executive_summary,
        }

    def compare(self, old_result: dict[str, Any], new_result: dict[str, Any]) -> dict[str, Any]:
        old_distribution = old_result["land_distribution"]
        new_distribution = new_result["land_distribution"]
        urban_growth = new_distribution.get("urban", 0) - old_distribution.get("urban", 0)
        forest_loss = old_distribution.get("forest", 0) - new_distribution.get("forest", 0)
        trend_report = (
            f"Urban area changed by {urban_growth:+d}% and forest cover changed by {forest_loss:+d}%. "
            f"The newer scene shows {new_result['environment_score']}/100 environmental score versus {old_result['environment_score']}/100 previously."
        )
        return {
            "urban_growth": urban_growth,
            "forest_loss": forest_loss,
            "report": trend_report,
        }
