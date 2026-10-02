from .registry import tool


@tool(
    name="estimate_trip_cost",
    description="Estimate total trip cost in GHS based on duration and travel style",
    parameters={
        "type": "object",
        "properties": {
            "days": {"type": "integer", "description": "Number of days"},
            "travel_style": {
                "type": "string",
                "enum": ["budget", "mid-range", "luxury"],
                "description": "Travel style / budget tier",
            },
            "regions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Regions or cities to visit",
            },
        },
        "required": ["days"],
    },
)
def estimate_trip_cost(
    days: int,
    travel_style: str = "mid-range",
    regions: list[str] | None = None,
) -> dict:
    if regions is None:
        regions = ["Accra"]
    daily_rates = {
        "budget": {"accommodation": 200, "food": 80, "local_transport": 30, "activities": 50},
        "mid-range": {"accommodation": 600, "food": 150, "local_transport": 60, "activities": 100},
        "luxury": {"accommodation": 1500, "food": 300, "local_transport": 120, "activities": 250},
    }
    rates = daily_rates.get(travel_style, daily_rates["mid-range"])
    daily_total = sum(rates.values())
    total = daily_total * days
    return {
        "style": travel_style,
        "days": days,
        "daily_estimate_ghs": daily_total,
        "total_estimate_ghs": total,
        "breakdown": rates,
        "note": "Does not include international flights or visa fees",
    }
