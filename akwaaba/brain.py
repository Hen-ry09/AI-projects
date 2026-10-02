from pathlib import Path


class Brain:
    def __init__(self, brain_dir: Path):
        self.brain_dir = brain_dir
        self.identity = self._read("brain.md")
        self.reasoning = self._read("reasoning.md")
        self.workflows = self._read("workflows.md")

    def _read(self, filename: str) -> str:
        path = self.brain_dir / filename
        if path.exists():
            return path.read_text().strip()
        return ""

    def build_system_prompt(self, skills_context: str) -> str:
        parts = [
            self.identity,
            "",
            "## How to Think & Reason",
            self.reasoning,
            "",
            "## Multi-Skill Workflows",
            self.workflows,
            "",
            "## Available Skills",
            skills_context,
        ]
        return "\n\n".join(p for p in parts if p)
