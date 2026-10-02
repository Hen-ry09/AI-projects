from .registry import tool

SEASONS: dict[str, dict[str, str]] = {
    "Accra": {
        "Nov–Mar": "Dry season — hot and sunny, best time to visit",
        "Apr–Jun": "First rainy season — humid, afternoon showers",
        "Jul–Aug": "Cooler but still some rain",
        "Sep–Oct": "Short dry spell before second rains",
    },
    "Kumasi": {
        "Nov–Mar": "Dry season — warm days, cool nights",
        "Apr–Jul": "Heavy rains — very humid, muddy roads",
        "Aug–Oct": "Light rains, cooler temperatures",
    },
    "Tamale": {
        "Nov–Mar": "Dry season — very hot, dusty (Harmattan winds)",
        "Apr–Oct": "Rainy season — hot and humid",
    },
}


@tool(
    name="get_weather_advice",
    description="Get seasonal weather advice for a Ghanaian region",
    parameters={
        "type": "object",
        "properties": {
            "region": {"type": "string", "description": "Region or city name (Accra, Kumasi, Tamale)"},
            "month": {"type": "string", "description": "Month name or abbreviation for specific advice"},
        },
        "required": ["region"],
    },
)
def get_weather_advice(region: str, month: str | None = None) -> dict:
    region = region.title()
    if region not in SEASONS:
        return {"region": region, "advice": "Weather data not available for this region"}
    seasons = SEASONS[region]
    if month:
        for period, description in seasons.items():
            if month[:3] in period:
                return {"region": region, "period": period, "advice": description}
    return {
        "region": region,
        "seasons": seasons,
        "general_advice": "Pack light clothing, rain gear if traveling in rainy season, and a light jacket for harmattan (Dec–Feb) in northern regions.",
    }
