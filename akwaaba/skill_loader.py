from pathlib import Path


class SkillDef:
    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.content = path.read_text() if path.exists() else ""


class SkillLoader:
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.skills: list[SkillDef] = []
        self._load()

    def _load(self):
        if not self.skills_dir.exists():
            return
        for child in sorted(self.skills_dir.iterdir()):
            if child.is_dir():
                skill_file = child / "SKILL.md"
                if skill_file.exists():
                    self.skills.append(SkillDef(child.name, skill_file))

    def build_context(self) -> str:
        parts = []
        for skill in self.skills:
            parts.append(f"### {skill.name}")
            parts.append(skill.content)
        return "\n\n".join(parts)
