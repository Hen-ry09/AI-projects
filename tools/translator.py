import json
import os

from .registry import tool

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def get_phrasebook(language: str) -> dict:
    path = os.path.join(DATA_DIR, "phrases.json")
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        data = json.load(f)
    return data.get(language.lower(), {})


@tool(
    name="translate_phrase",
    description="Look up a Ghanaian language phrase translation and pronunciation",
    parameters={
        "type": "object",
        "properties": {
            "phrase": {"type": "string", "description": "The English phrase or word to translate (e.g., welcome, thank_you, good_morning)"},
            "language": {"type": "string", "enum": ["twi", "ga", "ewe"], "description": "Target Ghanaian language"},
            "category": {"type": "string", "description": "Category: greetings, common, numbers"},
        },
        "required": ["phrase", "language"],
    },
)
def translate_phrase(
    phrase: str,
    language: str,
    category: str | None = None,
) -> dict | None:
    phrasebook = get_phrasebook(language)
    normalized = phrase.lower().replace(" ", "_")

    if category and category in phrasebook:
        for eng_key, entry in phrasebook[category].items():
            if normalized == eng_key.lower() or normalized == entry.get("phrase", "").lower():
                return {"code": eng_key, "category": category, **entry}
        return None

    for cat_name, cat_data in phrasebook.items():
        for eng_key, entry in cat_data.items():
            if normalized == eng_key.lower() or normalized == entry.get("phrase", "").lower():
                return {"code": eng_key, "category": cat_name, **entry}

    return None


SUPPORTED_LANGUAGES = ["twi", "ga", "ewe"]
