from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EnvironmentalAnalysis:
    score: int
    interpretation: str
    factors: dict[str, Any]


class EnvironmentalAnalyzer:
    def analyze(self, distribution: dict[str, int]) -> EnvironmentalAnalysis:
        vegetation = distribution.get("agriculture", 0) + distribution.get("forest", 0)
        urban = distribution.get("urban", 0) + distribution.get("industrial", 0) + distribution.get("residential", 0)
        water = distribution.get("water", 0)
        barren = distribution.get("barren", 0)

        vegetation_factor = min(1.0, vegetation / 100.0)
        urban_pressure = min(1.0, urban / 100.0)
        water_factor = min(1.0, water / 100.0)
        barren_pressure = min(1.0, barren / 100.0)

        score = int(round(
            35 * vegetation_factor
            + 20 * water_factor
            + 20 * (1.0 - urban_pressure)
            + 15 * (1.0 - barren_pressure)
            + 10
        ))
        score = max(0, min(score, 100))

        if score >= 80:
            interpretation = "Good vegetation coverage, balanced land distribution, and low environmental stress."
        elif score >= 60:
            interpretation = "Moderate environmental quality with manageable urban pressure and visible ecological assets."
        elif score >= 40:
            interpretation = "Mixed environmental conditions with elevated land-use pressure and moderate ecological risk."
        else:
            interpretation = "High environmental stress with limited vegetation cover and stronger urban or barren land presence."

        return EnvironmentalAnalysis(
            score=score,
            interpretation=interpretation,
            factors={
                "vegetation_coverage": vegetation,
                "urban_density": urban,
                "water_availability": water,
                "barren_land": barren,
            },
        )
