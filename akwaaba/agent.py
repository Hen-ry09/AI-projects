import json
import sys
from pathlib import Path

from .settings import Settings
from .llm import LLMClient
from .brain import Brain
from .skill_loader import SkillLoader
from .memory_manager import MemoryManager
from .session_manager import SessionManager

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR.parent))


class Agent:
    def __init__(self, user_id: str | None = None):
        self.settings = Settings()
        self.llm = LLMClient(self.settings)
        self.brain = Brain(self.settings.brain_dir)
        self.skill_loader = SkillLoader(self.settings.skills_dir)
        user_id = user_id or self.settings.default_user_id
        self.memory = MemoryManager(self.settings.memory_dir, user_id)
        self.session = SessionManager(self.settings.sessions_dir, user_id)
        self._tool_map: dict[str, callable] = {}
        self._openai_tools: list[dict] = []
        self._load_tools()
        self._build_system_prompt()

    def _load_tools(self):
        from tools.registry import get_all_tools

        self._tool_map = {}
        self._openai_tools = []
        for tool_name, tool_def in get_all_tools().items():
            self._tool_map[tool_name] = tool_def
            self._openai_tools.append(tool_def.to_openai_schema())

    def _build_system_prompt(self):
        skills_context = self.skill_loader.build_context()
        memory_context = self.memory.to_context_string()

        prompt = self.brain.build_system_prompt(skills_context)
        prompt += f"\n\n## User Memory Context\n{memory_context}"

        self.system_prompt = prompt

    def _execute_tool(self, name: str, arguments: dict) -> str:
        tool = self._tool_map.get(name)
        if not tool:
            return json.dumps({"error": f"Unknown tool: {name}"})
        try:
            result = tool.execute(**arguments)
            return json.dumps(result, default=str, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    def chat(self, user_message: str) -> str:
        self.session.add_message("user", user_message)

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.session.get_conversation_history())
        messages.append({"role": "user", "content": user_message})

        while True:
            content, tool_calls = self.llm.chat(messages, self._openai_tools)

            if not tool_calls:
                self.session.add_message("assistant", content)
                return content

            self.session.add_assistant_tool_call(content, tool_calls)
            messages.append({"role": "assistant", "content": content})

            if tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {"name": tc["name"], "arguments": json.dumps(tc["arguments"])},
                        }
                        for tc in tool_calls
                    ],
                })

            for tc in tool_calls:
                result = self._execute_tool(tc["name"], tc["arguments"])
                self.session.add_tool_result(tc["id"], tc["name"], result)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "name": tc["name"],
                    "content": result,
                })
