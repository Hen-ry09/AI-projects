import json
from pathlib import Path


class MemoryManager:
    FILES = {
        "profile": "traveler_profile.json",
        "preferences": "preferences.json",
        "itineraries": "itineraries.json",
        "saved_places": "saved_places.json",
        "conversation_facts": "conversation_facts.json",
        "favorites": "favorites.json",
    }

    def __init__(self, memory_dir: Path, user_id: str):
        self.user_dir = memory_dir / user_id
        self.user_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, dict | list] = {}
        self._load_all()

    def _path(self, key: str) -> Path:
        return self.user_dir / self.FILES[key]

    def _load_all(self):
        for key, filename in self.FILES.items():
            path = self.user_dir / filename
            if path.exists():
                with open(path) as f:
                    self._cache[key] = json.load(f)
            else:
                self._cache[key] = {} if key != "itineraries" else []

    def save(self, key: str):
        path = self._path(key)
        with open(path, "w") as f:
            json.dump(self._cache[key], f, indent=2)

    def get(self, key: str) -> dict | list:
        return self._cache.get(key, {} if key != "itineraries" else [])

    def set(self, key: str, value: dict | list):
        self._cache[key] = value
        self.save(key)

    def update(self, key: str, updates: dict):
        current = self._cache.get(key, {})
        if isinstance(current, dict):
            current.update(updates)
            self._cache[key] = current
            self.save(key)

    def append(self, key: str, item: dict | list):
        current = self._cache.get(key, [])
        if isinstance(current, list):
            current.append(item)
            self._cache[key] = current
            self.save(key)

    def to_context_string(self) -> str:
        parts = []
        for key in self.FILES:
            val = self._cache.get(key)
            if val and (isinstance(val, dict) and val) or (isinstance(val, list) and val):
                parts.append(f"### {key}\n{json.dumps(val, indent=2)}")
        return "\n\n".join(parts) if parts else "No saved memory yet."
