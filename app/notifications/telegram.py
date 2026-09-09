from __future__ import annotations

from app.models.auction import AuctionListing


def format_deal_alert(
    listing: AuctionListing,
    estimated_parts: float,
    estimated_repairs: float,
    estimated_total_cost: float,
    estimated_resale: float,
    estimated_gross_profit: float,
    maximum_bid: float,
    deal_score: int,
    risk_level: str,
) -> str:
    return (
        "🚗 VEHICLE DEAL FOUND\n"
        f"Auction: {listing.auction_source}\n"
        f"Year/Make/Model: {listing.vehicle.year} {listing.vehicle.make} {listing.vehicle.model}\n"
        f"Mileage: {listing.vehicle.mileage or 'N/A'}\n"
        f"Location: {listing.auction_location_name}\n"
        f"Distance: {listing.distance_miles or 'N/A'} miles\n"
        f"Damage: {listing.damage.primary_damage or 'N/A'}\n"
        f"Secondary Damage: {listing.damage.secondary_damage or 'N/A'}\n"
        f"Status: {listing.damage.run_and_drive or 'N/A'}\n"
        f"Transmission: {listing.vehicle.transmission or 'N/A'}\n"
        f"Current Bid: {listing.current_bid or 'N/A'}\n"
        f"Buy Now: {listing.buy_now_price or 'N/A'}\n"
        f"Estimated Final Bid: {listing.estimated_final_bid or 'N/A'}\n"
        f"Estimated Parts: {estimated_parts}\n"
        f"Estimated Repairs: {estimated_repairs}\n"
        f"Estimated Total Cost: {estimated_total_cost}\n"
        f"Estimated Resale: {estimated_resale}\n"
        f"Estimated Gross Profit: {estimated_gross_profit}\n"
        f"Maximum Recommended Bid: {maximum_bid}\n"
        f"Deal Score: {deal_score}/100\n"
        f"Risk: {risk_level}\n"
        f"Auction Date: {listing.auction_date.isoformat() if listing.auction_date else 'N/A'}\n"
        f"Listing: {listing.listing_url}"
    )
