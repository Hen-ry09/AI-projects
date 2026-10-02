import json
import os
from pathlib import Path

import dotenv

dotenv.load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings:
    def __init__(self):
        self.root_dir = ROOT_DIR
        self._settings_data = self._load_settings()
        self._validate()

    def _load_settings(self) -> dict:
        path = ROOT_DIR / "settings.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return {}

    def _validate(self):
        if not os.getenv("OPENAI_API_KEY"):
            print("Warning: OPENAI_API_KEY not set in .env file")

    @property
    def openai_api_key(self) -> str:
        return os.getenv("OPENAI_API_KEY", "")

    @property
    def openai_base_url(self) -> str:
        return self._settings_data.get("openai", {}).get("base_url", "https://openrouter.ai/api/v1")

    @property
    def openai_model(self) -> str:
        return os.getenv("OPENAI_MODEL") or self._settings_data.get("openai", {}).get("model", "gpt-4o-mini")

    @property
    def openai_temperature(self) -> float:
        return self._settings_data.get("openai", {}).get("temperature", 0.7)

    @property
    def openai_max_tokens(self) -> int:
        return self._settings_data.get("openai", {}).get("max_tokens", 1000)

    @property
    def default_user_id(self) -> str:
        return self._settings_data.get("default_user_id", "default")

    @property
    def data_dir(self) -> Path:
        return ROOT_DIR / "data"

    @property
    def memory_dir(self) -> Path:
        return ROOT_DIR / "memory"

    @property
    def sessions_dir(self) -> Path:
        return ROOT_DIR / "sessions"

    @property
    def skills_dir(self) -> Path:
        return ROOT_DIR / "skills"

    @property
    def knowledge_dir(self) -> Path:
        return ROOT_DIR / "knowledge"

    @property
    def brain_dir(self) -> Path:
        return ROOT_DIR / "brain"
