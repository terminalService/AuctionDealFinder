from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.models.damage import DamageReport
from app.models.vehicle import Vehicle


@dataclass(slots=True)
class AuctionListing:
    auction_source: str
    listing_url: str
    lot_number: str
    vehicle: Vehicle
    damage: DamageReport
    sale_type: str
    current_bid: float | None
    buy_now_price: float | None
    estimated_final_bid: float | None
    auction_date: datetime | None
    auction_location_name: str
    auction_location_address: str
    latitude: float
    longitude: float
    distance_miles: float | None
    distance_method: str
    title_type: str | None
    seller: str | None
    photo_urls: list[str]
    vehicle_description: str | None
