# Budget Planner

## Description
Estimate trip costs to Ghana including transportation, accommodation, food, activities, and miscellaneous expenses.

## Triggers
- "how much does a trip to Ghana cost"
- "budget for [N] days in Ghana"
- "cost of living in Accra"
- "cheapest way to travel Ghana"
- "budget breakdown for Ghana trip"
- "how much do hotels cost in Ghana"

## Workflow

1. **Gather inputs**: Duration, travel style (budget/mid-range/luxury), regions, group size, season
2. **Consult data**: Read `data/transport.json`, `data/attractions.json`, `data/hotels.json`, `data/restaurants.json`
3. **Build estimate**:
   - International flights (estimate based on region of origin)
   - Domestic transport (trotro, taxi, bus, domestic flights)
   - Accommodation per night × nights
   - Food: meals per day × cost per meal
   - Activities: entrance fees, tours, guides
   - Miscellaneous: SIM card, souvenirs, tips, emergencies
4. **Present breakdown**: Table or categorized list with low/mid/high ranges
5. **Money tips**: ATMs, mobile money (MoMo), currency exchange, tipping norms
