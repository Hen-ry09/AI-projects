# Memory Management

## Description
Manage user preferences, saved places, favorites, travel history, and personal profile data for personalized recommendations.

## Triggers
- "save this attraction"
- "remember my preference"
- "what have I saved"
- "show my favorites"
- "my previous trips"
- "update my profile"
- "remember that I like [something]"
- "what do you know about me"

## Capabilities
- Save and retrieve user preferences (budget tier, cuisine preferences, travel style)
- Save favorite attractions, hotels, restaurants
- Track previous itineraries and trips
- Store conversation facts for personalization
- Maintain traveler profile (nationality, interests, group size)

## Workflow
1. Identify the memory operation: save, retrieve, update, or delete
2. Access the appropriate memory file via MemoryManager
3. Acknowledge the save/update and summarize what's stored
4. Use stored preferences to personalize current recommendations
5. When the user asks "what do you know about me", summarize all stored data
