# Food Guide

## Description
Recommend Ghanaian dishes, restaurants, street food, and dining etiquette.

## Triggers
- "what food to eat in Ghana"
- "Ghanaian dishes"
- "best restaurants in [city]"
- "street food in Accra"
- "jollof rice in Ghana"
- "fufu"
- "Ghanaian food etiquette"
- "vegetarian options in Ghana"
- "local drinks in Ghana"

## Dependencies
- data/restaurants.json
- knowledge/food/

## Workflow
1. Identify what the user wants: dish recommendations, restaurant search, or dining etiquette
2. For dishes: describe popular Ghanaian dishes, ingredients, and where to try them
3. For restaurants: search `data/restaurants.json` by city and cuisine
4. For street food: recommend popular spots and hygiene tips
5. Include eating etiquette (right hand, communal eating, etc.)
6. Suggest local beverages (sobolo, palm wine, akpeteshie)
