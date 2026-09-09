from __future__ import annotations


def calculate_maximum_bid(
    estimated_vehicle_value: float,
    estimated_total_repair_cost: float,
    auction_fees: float,
    transportation: float,
    desired_profit: float,
    risk_factor: float,
) -> float:
    return max(
        0.0,
        estimated_vehicle_value
        - estimated_total_repair_cost
        - auction_fees
        - transportation
        - desired_profit
        - risk_factor,
    )
