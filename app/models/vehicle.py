from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Vehicle:
    year: int
    make: str
    model: str
    trim: str | None
    vin: str | None
    mileage: int | None
    engine: str | None
    transmission: str | None
    drivetrain: str | None
    fuel_type: str | None
