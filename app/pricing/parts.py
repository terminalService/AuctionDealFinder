from __future__ import annotations

from abc import ABC, abstractmethod


class PartsEstimator(ABC):
    @abstractmethod
    def estimate_parts_cost(self, make: str, model: str, damage_type: str) -> float:
        raise NotImplementedError


class StaticPartsEstimator(PartsEstimator):
    def __init__(self, fallback_cost: float = 1000.0):
        self.fallback_cost = fallback_cost

    def estimate_parts_cost(self, make: str, model: str, damage_type: str) -> float:
        _ = (make, model, damage_type)
        return self.fallback_cost
