import os

SKILL_DIR = os.path.join(os.path.dirname(__file__), "myskill")


def build_system_prompt() -> str | None:
    path = os.path.join(SKILL_DIR, "system-prompt.md")
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return f.read()
