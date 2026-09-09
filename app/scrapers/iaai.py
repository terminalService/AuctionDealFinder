from __future__ import annotations

from app.models.auction import AuctionListing
from app.scrapers.base import AuctionSource


class IAAISource(AuctionSource):
    source_name = "iaai"

    def fetch_listings(self) -> list[AuctionListing]:
        return []
