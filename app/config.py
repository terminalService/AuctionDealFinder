from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class AppConfig:
    max_buy_now_price: int = 3000
    max_current_bid: int = 3000
    max_estimated_bid: int = 4000
    max_distance_miles: int = 150
    min_deal_score: int = 70
    scan_interval_minutes: int = 15
    repair_contingency_percent: int = 20
    desired_profit: int = 2500
    preferred_makes: list[str] = field(default_factory=list)
    preferred_models: list[str] = field(default_factory=list)
    excluded_makes: list[str] = field(default_factory=list)
    excluded_damage_types: list[str] = field(default_factory=lambda: [
        "severe frame damage",
        "burn/fire damage",
        "engine seized",
        "engine missing",
        "transmission missing",
        "parts-only",
        "non-repairable",
        "excessive structural damage",
        "missing major components",
    ])
    maximum_mileage: int | None = None
    minimum_profit: int = 0
    maximum_repair_cost: int | None = None
    database_url: str = "sqlite:///data/auction_deals.db"
    log_level: str = "INFO"


@dataclass(slots=True)
class Secrets:
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None


def _read_simple_env(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not env_path.exists():
        return values
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def load_config(config_path: Path | str = "config.yaml") -> AppConfig:
    path = Path(config_path)
    data: dict[str, Any] = {}
    if path.exists():
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            data = loaded
    return AppConfig(**{k: v for k, v in data.items() if hasattr(AppConfig, k)})


def load_secrets(env_path: Path | str = ".env") -> Secrets:
    env_values = _read_simple_env(Path(env_path))
    return Secrets(
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", env_values.get("TELEGRAM_BOT_TOKEN")),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", env_values.get("TELEGRAM_CHAT_ID")),
    )
