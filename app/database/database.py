from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS auction_locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    UNIQUE(source, name, address)
);

CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vin TEXT,
    year INTEGER NOT NULL,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    trim TEXT,
    mileage INTEGER,
    engine TEXT,
    transmission TEXT,
    drivetrain TEXT,
    fuel_type TEXT,
    UNIQUE(vin, year, make, model, trim)
);

CREATE TABLE IF NOT EXISTS auction_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auction_source TEXT NOT NULL,
    listing_url TEXT NOT NULL,
    lot_number TEXT NOT NULL,
    vehicle_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    sale_type TEXT,
    current_bid REAL,
    previous_bid REAL,
    buy_now_price REAL,
    estimated_final_bid REAL,
    auction_date TEXT,
    title_type TEXT,
    seller TEXT,
    vehicle_status TEXT,
    first_seen TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    auction_status TEXT NOT NULL DEFAULT 'active',
    UNIQUE(auction_source, lot_number),
    FOREIGN KEY(vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY(location_id) REFERENCES auction_locations(id)
);

CREATE TABLE IF NOT EXISTS vehicle_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    image_rank INTEGER NOT NULL,
    FOREIGN KEY(listing_id) REFERENCES auction_listings(id),
    UNIQUE(listing_id, image_url)
);

CREATE TABLE IF NOT EXISTS damage_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    primary_damage TEXT,
    secondary_damage TEXT,
    run_and_drive TEXT,
    keys_status TEXT,
    image_damage_confidence REAL,
    image_damage_summary TEXT,
    flood_risk_level TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(listing_id) REFERENCES auction_listings(id)
);

CREATE TABLE IF NOT EXISTS parts_estimates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    parts_cost REAL,
    pricing_basis TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(listing_id) REFERENCES auction_listings(id)
);

CREATE TABLE IF NOT EXISTS repair_estimates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    parts_cost REAL,
    labor_estimate REAL,
    paint_body_estimate REAL,
    electrical_estimate REAL,
    miscellaneous_cost REAL,
    estimated_repair_cost REAL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(listing_id) REFERENCES auction_listings(id)
);

CREATE TABLE IF NOT EXISTS price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    previous_bid REAL,
    current_bid REAL,
    buy_now_price REAL,
    changed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(listing_id) REFERENCES auction_listings(id)
);

CREATE TABLE IF NOT EXISTS deal_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    reasons_json TEXT NOT NULL,
    risks_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(listing_id) REFERENCES auction_listings(id)
);

CREATE TABLE IF NOT EXISTS telegram_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    alert_type TEXT NOT NULL,
    telegram_message_id TEXT,
    sent_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(listing_id) REFERENCES auction_listings(id),
    UNIQUE(listing_id, alert_type)
);
"""


class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()
