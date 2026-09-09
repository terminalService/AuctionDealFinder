# AuctionDealFinder

AuctionDealFinder is a modular Python application scaffold for monitoring vehicle auction opportunities from Copart and IAAI.

## Phase 1 Included

- Clean application structure under `/app`
- Config loader from `config.yaml` and `.env`
- SQLite database schema with required Phase 1 tables
- Auction source abstraction + fixture-based development source
- 20 realistic mock listings in `data/mock_listings.json`
- Initial repository and model wiring for storing listings and price history
- Unit tests for config, fixture loading, and database upsert behavior

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main --dev
```

### Run tests

```bash
pytest -q
```

## Configuration

- Runtime settings: `config.yaml`
- Secrets template: `.env.example`

Never commit real Telegram credentials. Use a local `.env` file only.

## Development mode

`--dev` reads from `data/mock_listings.json` instead of live auction sources.

```bash
python -m app.main --dev --fixture-path data/mock_listings.json --db-path data/auction_deals.db
```

## Notes

- Live Copart/IAAI adapters are intentionally stubbed in Phase 1.
- No CAPTCHA bypassing, authentication bypassing, or anti-bot circumvention is implemented.
- The system is designed for manual review support, not automatic bidding.
