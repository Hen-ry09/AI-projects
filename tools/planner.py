from datetime import date, timedelta

from .registry import tool

TRAVEL_TIMES: dict[str, dict[str, str]] = {
    "Accra": {"Cape Coast": "2.5–3 hrs", "Kumasi": "4–5 hrs", "Takoradi": "3.5–4 hrs"},
    "Cape Coast": {"Accra": "2.5–3 hrs", "Kumasi": "5–6 hrs"},
    "Kumasi": {"Accra": "4–5 hrs", "Cape Coast": "5–6 hrs", "Tamale": "6–8 hrs"},
    "Tamale": {"Kumasi": "6–8 hrs", "Accra": "10–12 hrs"},
}


@tool(
    name="estimate_travel_time",
    description="Estimate travel time between two Ghanaian cities",
    parameters={
        "type": "object",
        "properties": {
            "origin": {"type": "string", "description": "Departure city"},
            "destination": {"type": "string", "description": "Arrival city"},
        },
        "required": ["origin", "destination"],
    },
)
def estimate_travel_time(origin: str, destination: str) -> str:
    origin = origin.title()
    destination = destination.title()
    if origin in TRAVEL_TIMES and destination in TRAVEL_TIMES[origin]:
        return TRAVEL_TIMES[origin][destination]
    if destination in TRAVEL_TIMES and origin in TRAVEL_TIMES[destination]:
        return TRAVEL_TIMES[destination][origin]
    return "Unknown — approximately 4–6 hours"


@tool(
    name="build_itinerary",
    description="Build a day-by-day itinerary skeleton for a Ghana trip",
    parameters={
        "type": "object",
        "properties": {
            "start_date": {"type": "string", "description": "Trip start date (YYYY-MM-DD)"},
            "days": {"type": "integer", "description": "Number of days"},
            "locations": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of cities/regions to visit in order",
            },
        },
        "required": ["start_date", "days", "locations"],
    },
)
def build_itinerary(start_date: str, days: int, locations: list[str]) -> list[dict]:
    itinerary = []
    current = date.fromisoformat(start_date)
    for i in range(days):
        location = locations[i % len(locations)] if locations else "Accra"
        itinerary.append({
            "day": i + 1,
            "date": current.isoformat(),
            "location": location,
            "notes": "",
        })
        current += timedelta(days=1)
    return itinerary
