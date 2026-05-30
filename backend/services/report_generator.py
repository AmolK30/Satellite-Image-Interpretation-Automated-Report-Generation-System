from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from backend.services.classifier import ClassificationResult
from backend.services.disaster_detector import DisasterAssessment
from backend.services.environmental_analyzer import EnvironmentalAnalysis


@dataclass(frozen=True)
class ReportBundle:
    report_text: str
    executive_summary: str


class ReportGenerator:
    def generate(
        self,
        image_name: str,
        classification: ClassificationResult,
        environmental: EnvironmentalAnalysis,
        disaster: DisasterAssessment,
        comparison: dict[str, Any] | None = None,
    ) -> ReportBundle:
        distribution_lines = [
            f"- {label.replace('_', ' ').title()}: {value}%"
            for label, value in sorted(classification.distribution.items(), key=lambda item: item[1], reverse=True)
            if value > 0
        ]

        observation_lines = []
        if classification.distribution.get("agriculture", 0) >= max(classification.distribution.values()):
            observation_lines.append("Agricultural cover dominates the scene, suggesting active land management or crop presence.")
        if classification.distribution.get("urban", 0) + classification.distribution.get("residential", 0) > 35:
            observation_lines.append("Urban development is significant and should be tracked for expansion pressure.")
        if environmental.score >= 75:
            observation_lines.append("Environmental indicators remain favorable with broad land-use balance.")
        elif environmental.score <= 50:
            observation_lines.append("Environmental stress indicators warrant closer review and mitigation planning.")
        if disaster.risk_level == "High":
            observation_lines.append("The site shows elevated disaster susceptibility and needs monitoring.")

        comparison_section = ""
        if comparison:
            comparison_section = "\n\nUrban Expansion Analysis:\n" + "\n".join(
                f"- {key.replace('_', ' ').title()}: {value}" for key, value in comparison.items() if key != "report"
            )

        report_text = (
            f"Executive Summary:\n"
            f"Satellite image {image_name} indicates a dominant land cover pattern of {classification.dominant_class.replace('_', ' ')}. "
            f"The environmental score is {environmental.score}/100, which reflects {environmental.interpretation.lower()}\n\n"
            f"Land Use Distribution:\n"
            + "\n".join(distribution_lines)
            + "\n\nObservations:\n"
            + "\n".join(f"- {line}" for line in observation_lines or ["Scene characteristics are consistent with the computed land-use distribution."])
            + f"\n\nRisk Assessment:\n- {disaster.risk_level} risk detected."
            + comparison_section
            + "\n\nRecommendations:\n"
            + "\n".join(f"- {item}" for item in disaster.recommendations)
            + f"\n\nEnvironmental Score: {environmental.score}/100\nGenerated: {datetime.now(timezone.utc).isoformat()}"
        )

        summary = (
            f"{classification.dominant_class.replace('_', ' ').title()} is the leading land-use category, "
            f"with an environmental score of {environmental.score}/100 and {disaster.risk_level.lower()} disaster risk."
        )
        return ReportBundle(report_text=report_text, executive_summary=summary)
