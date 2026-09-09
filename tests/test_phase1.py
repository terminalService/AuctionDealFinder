from __future__ import annotations

from pathlib import Path

from app.config import load_config
from app.database.database import Database
from app.database.repositories import ListingRepository
from app.scrapers.base import FixtureAuctionSource


def test_load_config_from_yaml(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    config_file.write_text("max_buy_now_price: 2500\nscan_interval_minutes: 10\n", encoding="utf-8")

    config = load_config(config_file)

    assert config.max_buy_now_price == 2500
    assert config.scan_interval_minutes == 10
    assert config.max_current_bid == 3000


def test_fixture_contains_at_least_20_listings() -> None:
    source = FixtureAuctionSource(Path("data/mock_listings.json"))
    listings = source.fetch_listings()

    assert len(listings) >= 20
    assert {l.auction_source for l in listings} == {"copart", "iaai"}


def test_database_schema_and_upsert(tmp_path: Path) -> None:
    db = Database(tmp_path / "test.db")
    db.initialize()

    source = FixtureAuctionSource(Path("data/mock_listings.json"))
    listings = source.fetch_listings()

    repo = ListingRepository(db)
    inserted_first = repo.upsert_listings(listings[:2])
    inserted_second = repo.upsert_listings(listings[:2])

    assert inserted_first == 2
    assert inserted_second == 2

    with db.connect() as conn:
        count = conn.execute("SELECT COUNT(*) AS c FROM auction_listings").fetchone()["c"]
        assert count == 2

        history = conn.execute("SELECT COUNT(*) AS c FROM price_history").fetchone()["c"]
        assert history == 4
