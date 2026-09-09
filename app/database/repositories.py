from __future__ import annotations

from app.database.database import Database
from app.models.auction import AuctionListing


class ListingRepository:
    def __init__(self, database: Database):
        self.database = database

    def upsert_listings(self, listings: list[AuctionListing]) -> int:
        count = 0
        with self.database.connect() as conn:
            for listing in listings:
                location_id = self._upsert_location(conn, listing)
                vehicle_id = self._upsert_vehicle(conn, listing)
                listing_id = self._upsert_listing(conn, listing, vehicle_id, location_id)
                self._upsert_images(conn, listing_id, listing.photo_urls)
                self._insert_damage(conn, listing_id, listing)
                count += 1
            conn.commit()
        return count

    @staticmethod
    def _upsert_location(conn, listing: AuctionListing) -> int:
        conn.execute(
            """
            INSERT INTO auction_locations(source, name, address, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(source, name, address)
            DO UPDATE SET latitude = excluded.latitude, longitude = excluded.longitude
            """,
            (
                listing.auction_source,
                listing.auction_location_name,
                listing.auction_location_address,
                listing.latitude,
                listing.longitude,
            ),
        )
        row = conn.execute(
            "SELECT id FROM auction_locations WHERE source = ? AND name = ? AND address = ?",
            (listing.auction_source, listing.auction_location_name, listing.auction_location_address),
        ).fetchone()
        return int(row["id"])

    @staticmethod
    def _upsert_vehicle(conn, listing: AuctionListing) -> int:
        v = listing.vehicle
        conn.execute(
            """
            INSERT INTO vehicles(vin, year, make, model, trim, mileage, engine, transmission, drivetrain, fuel_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(vin, year, make, model, trim)
            DO UPDATE SET mileage = excluded.mileage, engine = excluded.engine,
                          transmission = excluded.transmission, drivetrain = excluded.drivetrain,
                          fuel_type = excluded.fuel_type
            """,
            (v.vin, v.year, v.make, v.model, v.trim, v.mileage, v.engine, v.transmission, v.drivetrain, v.fuel_type),
        )
        row = conn.execute(
            "SELECT id FROM vehicles WHERE vin IS ? AND year = ? AND make = ? AND model = ? AND trim IS ?",
            (v.vin, v.year, v.make, v.model, v.trim),
        ).fetchone()
        return int(row["id"])

    @staticmethod
    def _upsert_listing(conn, listing: AuctionListing, vehicle_id: int, location_id: int) -> int:
        conn.execute(
            """
            INSERT INTO auction_listings(
                auction_source, listing_url, lot_number, vehicle_id, location_id,
                sale_type, current_bid, buy_now_price, estimated_final_bid, auction_date,
                title_type, seller, vehicle_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(auction_source, lot_number)
            DO UPDATE SET
                listing_url = excluded.listing_url,
                previous_bid = auction_listings.current_bid,
                current_bid = excluded.current_bid,
                buy_now_price = excluded.buy_now_price,
                estimated_final_bid = excluded.estimated_final_bid,
                auction_date = excluded.auction_date,
                title_type = excluded.title_type,
                seller = excluded.seller,
                vehicle_status = excluded.vehicle_status,
                last_seen = CURRENT_TIMESTAMP
            """,
            (
                listing.auction_source,
                listing.listing_url,
                listing.lot_number,
                vehicle_id,
                location_id,
                listing.sale_type,
                listing.current_bid,
                listing.buy_now_price,
                listing.estimated_final_bid,
                listing.auction_date.isoformat() if listing.auction_date else None,
                listing.title_type,
                listing.seller,
                listing.damage.run_and_drive,
            ),
        )
        row = conn.execute(
            "SELECT id FROM auction_listings WHERE auction_source = ? AND lot_number = ?",
            (listing.auction_source, listing.lot_number),
        ).fetchone()
        listing_id = int(row["id"])
        conn.execute(
            """
            INSERT INTO price_history(listing_id, previous_bid, current_bid, buy_now_price)
            VALUES (?, ?, ?, ?)
            """,
            (listing_id, None, listing.current_bid, listing.buy_now_price),
        )
        return listing_id

    @staticmethod
    def _upsert_images(conn, listing_id: int, photo_urls: list[str]) -> None:
        for index, image_url in enumerate(photo_urls):
            conn.execute(
                """
                INSERT INTO vehicle_images(listing_id, image_url, image_rank)
                VALUES (?, ?, ?)
                ON CONFLICT(listing_id, image_url)
                DO UPDATE SET image_rank = excluded.image_rank
                """,
                (listing_id, image_url, index),
            )

    @staticmethod
    def _insert_damage(conn, listing_id: int, listing: AuctionListing) -> None:
        d = listing.damage
        conn.execute(
            """
            INSERT INTO damage_assessments(
                listing_id, primary_damage, secondary_damage, run_and_drive,
                keys_status, image_damage_confidence, image_damage_summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                listing_id,
                d.primary_damage,
                d.secondary_damage,
                d.run_and_drive,
                d.keys_status,
                d.image_damage_confidence,
                d.image_damage_summary,
            ),
        )
