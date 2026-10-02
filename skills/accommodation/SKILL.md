# Accommodation Guide

## Description
Recommend hotels, lodges, guesthouses, and eco-lodges in Ghana based on city, budget tier, and preferences.

## Triggers
- "where to stay in [city]"
- "hotels in Accra"
- "budget accommodation in Ghana"
- "luxury resorts in Ghana"
- "eco-lodges in Ghana"
- "places to stay near Mole National Park"
- "recommend a hotel in Kumasi"

## Dependencies
- data/hotels.json
- knowledge/accommodation/

## Workflow
1. Ask about city, budget tier, and any preferences (pool, beach, nature, etc.) if not provided
2. Search `data/hotels.json` for matching options
3. Read relevant `knowledge/accommodation/*.md` for additional context
4. Present options with price range, features, and rating
5. Offer to book or save favorites
