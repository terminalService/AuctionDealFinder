from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DealScoreBreakdown:
    score: int
    reasons: list[str]
    risks: list[str]
