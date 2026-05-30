from __future__ import annotations

from dataclasses import dataclass

from backend.services.feature_extractor import ImageFeatures


LAND_COVER_LABELS = [
    "agriculture",
    "forest",
    "urban",
    "industrial",
    "water",
    "roads",
    "residential",
    "barren",
]


@dataclass(frozen=True)
class ClassificationResult:
    distribution: dict[str, int]
    confidence: float
    dominant_class: str
    raw_scores: dict[str, float]


class LandCoverClassifier:
    """Rule-based classifier with optional hooks for deep models."""

    def __init__(self) -> None:
        self.labels = LAND_COVER_LABELS

    def classify(self, features: ImageFeatures) -> ClassificationResult:
        raw_scores = {
            "agriculture": max(0.05, features.vegetation_index * 0.45 + (1.0 - features.urban_index) * 0.15 + (1.0 - features.water_index) * 0.1),
            "forest": max(0.05, features.vegetation_index * 0.55 + features.texture_score * 0.2),
            "urban": max(0.05, features.urban_index * 0.55 + features.edge_score * 0.2 + (1.0 - features.vegetation_index) * 0.1),
            "industrial": max(0.05, features.urban_index * 0.45 + features.barren_index * 0.2 + features.edge_score * 0.15),
            "water": max(0.05, features.water_index * 0.7),
            "roads": max(0.05, features.edge_score * 0.35 + features.urban_index * 0.15),
            "residential": max(0.05, features.urban_index * 0.4 + features.texture_score * 0.2 + features.vegetation_index * 0.1),
            "barren": max(0.05, features.barren_index * 0.6 + (1.0 - features.vegetation_index) * 0.1),
        }
        total = sum(raw_scores.values()) or 1.0
        distribution = {label: int(round(score / total * 100)) for label, score in raw_scores.items()}

        diff = 100 - sum(distribution.values())
        if diff != 0:
            top_label = max(distribution, key=distribution.get)
            distribution[top_label] += diff

        dominant_class = max(distribution, key=distribution.get)
        confidence = round(distribution[dominant_class] / 100.0, 2)
        return ClassificationResult(
            distribution=distribution,
            confidence=confidence,
            dominant_class=dominant_class,
            raw_scores={label: round(score, 4) for label, score in raw_scores.items()},
        )

    @staticmethod
    def summarize_distribution(distribution: dict[str, int]) -> list[str]:
        ordered = sorted(distribution.items(), key=lambda item: item[1], reverse=True)
        summary = []
        for label, value in ordered:
            if value <= 0:
                continue
            summary.append(f"{label.replace('_', ' ').title()}: {value}%")
        return summary
