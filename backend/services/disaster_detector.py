from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DisasterAssessment:
    risk_level: str
    threats: list[str]
    recommendations: list[str]


class DisasterDetector:
    def assess(self, distribution: dict[str, int], environmental_score: int) -> DisasterAssessment:
        water = distribution.get("water", 0)
        forest = distribution.get("forest", 0)
        barren = distribution.get("barren", 0)
        urban = distribution.get("urban", 0) + distribution.get("industrial", 0)

        threats: list[str] = []
        recommendations: list[str] = []

        if water < 8:
            threats.append("Potential drought stress or limited surface water.")
            recommendations.append("Prioritize water conservation and hydrological monitoring.")
        if forest < 12:
            threats.append("Possible deforestation or low tree cover.")
            recommendations.append("Preserve and expand green buffers.")
        if barren > 20:
            threats.append("Elevated barren land exposure, erosion, or soil degradation risk.")
            recommendations.append("Stabilize exposed land and restore vegetation where feasible.")
        if urban > 35:
            threats.append("High urban density may increase heat island and runoff risk.")
            recommendations.append("Monitor expansion corridors and drainage infrastructure.")

        if environmental_score >= 80 and not threats:
            risk_level = "Low"
            recommendations.append("Maintain current land management practices.")
        elif environmental_score >= 55:
            risk_level = "Moderate"
        else:
            risk_level = "High"

        if not recommendations:
            recommendations.append("Continue periodic monitoring using change-detection workflows.")

        return DisasterAssessment(
            risk_level=risk_level,
            threats=threats or ["No severe disaster indicators detected in the current scene."],
            recommendations=recommendations,
        )
