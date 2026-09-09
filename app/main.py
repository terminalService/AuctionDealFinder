from __future__ import annotations

import argparse
from pathlib import Path

from app.config import load_config, load_secrets
from app.database.database import Database
from app.database.repositories import ListingRepository
from app.scrapers.base import FixtureAuctionSource
from app.utils.logging import get_logger


logger = get_logger(__name__)


def run_dev_mode(data_path: Path, db_path: Path) -> int:
    config = load_config()
    _ = load_secrets()
    database = Database(db_path)
    database.initialize()

    source = FixtureAuctionSource(data_path)
    listings = source.fetch_listings()

    repo = ListingRepository(database)
    inserted = repo.upsert_listings(listings)

    logger.info(
        "Development scan complete",
        extra={
            "source": source.source_name,
            "listings_discovered": len(listings),
            "listings_upserted": inserted,
            "max_distance_miles": config.max_distance_miles,
            "scan_interval_minutes": config.scan_interval_minutes,
        },
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AuctionDealFinder")
    parser.add_argument("--dev", action="store_true", help="Use local fixture data")
    parser.add_argument(
        "--fixture-path",
        default="data/mock_listings.json",
        help="Path to fixture data JSON file",
    )
    parser.add_argument(
        "--db-path",
        default="data/auction_deals.db",
        help="SQLite database file path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.dev:
        return run_dev_mode(Path(args.fixture_path), Path(args.db_path))

    logger.error(
        "Live mode is not implemented in Phase 1. Use --dev with fixture data.",
        extra={"mode": "live"},
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
