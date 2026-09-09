from __future__ import annotations

from app.models.auction import AuctionListing
from app.scrapers.base import AuctionSource


class CopartSource(AuctionSource):
    source_name = "copart"

    def fetch_listings(self) -> list[AuctionListing]:
        return []
