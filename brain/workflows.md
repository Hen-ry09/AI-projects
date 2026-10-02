# Workflows — Multi-Skill Orchestration

## Common Workflow Patterns

### Full Trip Planning
**Skills involved**: itinerary-planner, attraction-search, accommodation, transportation, budget-planner, culture-guide, food-guide
**Flow**:
1. Gather trip parameters (duration, regions, budget, interests, traveler type)
2. Attraction-search → find things to do in each region
3. Accommodation → recommend places to stay per region and budget
4. Transportation → connect regions with travel options and times
5. Budget-planner → estimate total trip cost
6. Build day-by-day itinerary balancing activities, travel, and rest
7. Culture-guide → add local etiquette tips for each region
8. Food-guide → recommend local dishes and restaurants

### "What to do in [city]" (Quick Discovery)
**Skills involved**: attraction-search, food-guide, culture-guide
**Flow**:
1. Look up attractions for the city
2. Find notable restaurants or local dishes
3. Add cultural context or etiquette tips for that city

### Language Learning Session
**Skills involved**: language-helper, memory
**Flow**:
1. Identify desired language and topic (greetings, food, numbers)
2. Retrieve and teach phrases with pronunciation
3. Optionally quiz the user
4. Save learned phrases to user's memory for future review

### Budget Breakdown Request
**Skills involved**: budget-planner, accommodation, transportation, food-guide
**Flow**:
1. Gather trip details (duration, regions, travel style)
2. Estimate accommodation costs per region
3. Estimate transportation (intercity + local)
4. Estimate food costs
5. Estimate activity/attraction fees
6. Present comprehensive breakdown with low/mid/high ranges

### Emergency Information Request
**Skills involved**: travel-updates
**Flow**:
1. Categorize the emergency type (medical, safety, contact, etc.)
2. Provide relevant information from knowledge base
3. Include official contact numbers
4. Recommend verifying with current sources

### Memory-Enhanced Recommendations
**Skills involved**: memory, attraction-search, accommodation, food-guide
**Flow**:
1. Check user's profile, preferences, and history
2. Cross-reference with available data
3. Prioritize recommendations matching known preferences
4. Reference past trips if relevant

## Skill Chaining Rules

- When chaining skills, pass relevant context between them (location, budget, preferences)
- Only call skills that are necessary — don't over-engineer simple requests
- For simple queries (e.g., "how do you say hello in Twi"), use a single skill directly
- Save key facts to memory after significant interactions (new preferences, planned trips)
