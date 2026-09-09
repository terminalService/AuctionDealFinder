from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RepairEstimate:
    parts_cost: float
    labor_estimate: float
    paint_body_estimate: float
    electrical_estimate: float
    miscellaneous_cost: float

    @property
    def estimated_repair_cost(self) -> float:
        return (
            self.parts_cost
            + self.labor_estimate
            + self.paint_body_estimate
            + self.electrical_estimate
            + self.miscellaneous_cost
        )
