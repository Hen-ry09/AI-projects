# Itinerary Planner

## Description
Build day-by-day travel plans for Ghana trips based on duration, interests, budget, and regions of interest.

## Triggers
- "plan a trip to Ghana"
- "itinerary for [N] days"
- "what should I do in Accra for a weekend"
- "plan my honeymoon in Ghana"
- "travel route from Accra to Cape Coast"

## Workflow

1. **Gather inputs**: Travel dates, duration, group size, budget range, interests (culture, nature, food, history, nightlife, adventure), regions/cities of interest
2. **Consult data**: Load attractions, hotels, restaurants, transport from `data/`
3. **Check knowledge**: Read relevant `knowledge/attractions/*.md` and `knowledge/transportation/*.md`
4. **Build itinerary**:
   - Balance activities across days (not too packed)
   - Include realistic travel times between locations
   - Mix popular attractions with hidden gems
   - Recommend local restaurants and food experiences
   - Suggest accommodation options per budget tier
5. **Present results**: Day-by-day breakdown with morning/afternoon/evening slots, estimated costs, and travel tips
6. **Save to memory**: Store the plan in `memory/previous_trips.json`
