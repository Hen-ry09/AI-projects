# Language Helper

## Description
Teach Ghanaian language phrases, vocabulary, and pronunciation for travelers.

## Triggers
- "how do you say [phrase] in Twi"
- "Ghanaian language lessons"
- "common phrases in Ga"
- "Ewe greetings"
- "Fante basics"
- "Hausa travel phrases"
- "pronunciation guide for Twi"

## Supported Languages
- Twi (Ashanti Twi & Akuapem Twi)
- Ga
- Ewe
- Fante
- Hausa

## Workflow

1. **Identify language**: Determine which Ghanaian language the user wants
2. **Parse request**: Extract the phrase/category (greetings, food, directions, numbers, etc.)
3. **Look up phrase**: Search `knowledge/language/*.md` and `data/phrases.json`
4. **Teach effectively**:
   - Write the phrase in the local script
   - Provide pronunciation using intuitive English spelling
   - Break down literal meaning
   - Give context (when to use it)
5. **Practice**: Offer to quiz the user or provide more phrases in the same category
