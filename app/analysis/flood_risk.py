from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FloodRiskResult:
    score: int
    level: str


def classify_flood_risk(
    flood_reported: bool,
    engine_runs: bool,
    transmission_engages: bool,
    corrosion_visible: bool,
    water_intrusion_visible: bool,
) -> FloodRiskResult:
    score = 0
    if flood_reported:
        score += 35
    if corrosion_visible:
        score += 25
    if water_intrusion_visible:
        score += 20
    if not engine_runs:
        score += 10
    if not transmission_engages:
        score += 10

    if score < 30:
        level = "LOW FLOOD RISK"
    elif score < 60:
        level = "MEDIUM FLOOD RISK"
    else:
        level = "HIGH FLOOD RISK"

    return FloodRiskResult(score=score, level=level)
