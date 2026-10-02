# Attraction Search

## Description
Search and recommend Ghanaian attractions, landmarks, and activities based on user preferences.

## Triggers
- "what to do in [city/region]"
- "best attractions in Ghana"
- "beaches near Accra"
- "historical sites in Ghana"
- "national parks in Ghana"
- "hidden gems in [location]"

## Workflow

1. **Parse query**: Extract location, category (beach, history, nature, shopping, food, etc.), and any constraints
2. **Search data**: Query `data/attractions.json` and `knowledge/attractions/*.md`
3. **Filter & rank**: Match against user preferences and current context
4. **Present results**: Brief description, location, estimated entrance fees, best time to visit, tips
5. **Offer follow-up**: Ask if they want directions, nearby restaurants, or to add to an itinerary
