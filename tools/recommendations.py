from .registry import tool
from .search import search_attractions, search_hotels, search_restaurants


@tool(
    name="get_recommendations",
    description="Get personalized travel recommendations combining attractions, hotels, and restaurants for a city",
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name in Ghana"},
            "interests": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Interest categories (nature, history, beach, culture, food, etc.)",
            },
            "budget_tier": {
                "type": "string",
                "enum": ["budget", "mid-range", "luxury"],
                "description": "Preferred accommodation budget tier",
            },
        },
        "required": ["city"],
    },
)
def get_recommendations(
    city: str,
    interests: list[str] | None = None,
    budget_tier: str = "mid-range",
) -> dict:
    attractions = search_attractions(city=city)
    hotels = search_hotels(city=city, tier=budget_tier)
    restaurants = search_restaurants(city=city)

    if interests:
        attractions = [a for a in attractions if any(
            i.lower() in [c.lower() for c in a.get("category", [])]
            for i in interests
        )]

    return {
        "city": city,
        "attractions": attractions[:5],
        "hotels": hotels[:3],
        "restaurants": restaurants[:3],
    }
