from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from app.models.auction import AuctionListing
from app.models.damage import DamageReport
from app.models.vehicle import Vehicle


class AuctionSource(ABC):
    source_name: str

    @abstractmethod
    def fetch_listings(self) -> list[AuctionListing]:
        raise NotImplementedError


class FixtureAuctionSource(AuctionSource):
    source_name = "fixture"

    def __init__(self, fixture_path: Path):
        self.fixture_path = fixture_path

    def fetch_listings(self) -> list[AuctionListing]:
        raw_items = json.loads(self.fixture_path.read_text(encoding="utf-8"))
        listings: list[AuctionListing] = []
        for item in raw_items:
            vehicle = Vehicle(
                year=item["year"],
                make=item["make"],
                model=item["model"],
                trim=item.get("trim"),
                vin=item.get("vin"),
                mileage=item.get("mileage"),
                engine=item.get("engine"),
                transmission=item.get("transmission"),
                drivetrain=item.get("drivetrain"),
                fuel_type=item.get("fuel_type"),
            )
            damage = DamageReport(
                primary_damage=item.get("primary_damage"),
                secondary_damage=item.get("secondary_damage"),
                run_and_drive=item.get("run_and_drive"),
                keys_status=item.get("keys_status"),
                image_damage_confidence=item.get("image_damage_confidence"),
                image_damage_summary=item.get("image_damage_summary"),
            )
            listings.append(
                AuctionListing(
                    auction_source=item["auction_source"],
                    listing_url=item["listing_url"],
                    lot_number=item["lot_number"],
                    vehicle=vehicle,
                    damage=damage,
                    sale_type=item.get("sale_type", "Auction"),
                    current_bid=item.get("current_bid"),
                    buy_now_price=item.get("buy_now_price"),
                    estimated_final_bid=item.get("estimated_final_bid"),
                    auction_date=datetime.fromisoformat(item["auction_date"]) if item.get("auction_date") else None,
                    auction_location_name=item["auction_location_name"],
                    auction_location_address=item["auction_location_address"],
                    latitude=item["latitude"],
                    longitude=item["longitude"],
                    distance_miles=item.get("distance_miles"),
                    distance_method=item.get("distance_method", "haversine_approx"),
                    title_type=item.get("title_type"),
                    seller=item.get("seller"),
                    photo_urls=item.get("photo_urls", []),
                    vehicle_description=item.get("vehicle_description"),
                )
            )
        return listings
