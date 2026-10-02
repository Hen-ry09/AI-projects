import json
import os
from typing import Any

from .registry import tool

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _load_json(filename: str) -> Any:
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


@tool(
    name="search_attractions",
    description="Search Ghana attractions by city, category, or maximum entry fee",
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name (e.g., Accra, Cape Coast, Kumasi)"},
            "category": {"type": "string", "description": "Category: nature, history, beach, culture, adventure, heritage, museum, landmark, wildlife, entertainment, shopping, relaxation"},
            "max_budget": {"type": "number", "description": "Maximum entry fee in GHS"},
        },
    },
)
def search_attractions(
    city: str | None = None,
    category: str | None = None,
    max_budget: int | None = None,
) -> list[dict]:
    data = _load_json("attractions.json")
    results = data.get("attractions", [])
    if city:
        results = [a for a in results if a.get("city", "").lower() == city.lower()]
    if category:
        results = [
            a
            for a in results
            if any(cat.lower() == category.lower() for cat in a.get("category", []))
        ]
    if max_budget is not None:
        results = [
            a
            for a in results
            if a.get("entry_fee_ghs", {}).get("non_citizen", 0) <= max_budget
        ]
    return results


@tool(
    name="search_hotels",
    description="Search for hotels in Ghana by city and budget tier",
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"},
            "tier": {"type": "string", "enum": ["budget", "mid-range", "luxury"], "description": "Hotel tier"},
        },
    },
)
def search_hotels(
    city: str | None = None,
    tier: str | None = None,
    max_budget: int | None = None,
) -> list[dict]:
    data = _load_json("hotels.json")
    results = data.get("hotels", [])
    if city:
        results = [h for h in results if h.get("city", "").lower() == city.lower()]
    if tier:
        results = [h for h in results if h.get("tier", "").lower() == tier.lower()]
    return results


@tool(
    name="search_restaurants",
    description="Search for restaurants in Ghana by city and cuisine type",
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"},
            "cuisine": {"type": "string", "description": "Cuisine type (Ghanaian, seafood, continental, fusion, etc.)"},
        },
    },
)
def search_restaurants(
    city: str | None = None,
    cuisine: str | None = None,
) -> list[dict]:
    data = _load_json("restaurants.json")
    results = data.get("restaurants", [])
    if city:
        results = [r for r in results if r.get("city", "").lower() == city.lower()]
    if cuisine:
        results = [
            r
            for r in results
            if any(c.lower() == cuisine.lower() for c in r.get("cuisine", []))
        ]
    return results
