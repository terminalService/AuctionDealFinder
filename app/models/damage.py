from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DamageReport:
    primary_damage: str | None
    secondary_damage: str | None
    run_and_drive: str | None
    keys_status: str | None
    image_damage_confidence: float | None = None
    image_damage_summary: str | None = None
