import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


class SessionManager:
    def __init__(self, sessions_dir: Path, user_id: str):
        self.user_dir = sessions_dir / user_id
        self.user_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = str(uuid.uuid4())[:8]
        self.messages: list[dict] = []
        self._load_existing()

    def _load_existing(self):
        self.session_file = self.user_dir / f"{self.session_id}.json"
        if self.session_file.exists():
            with open(self.session_file) as f:
                data = json.load(f)
                self.messages = data.get("messages", [])

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self._persist()

    def add_tool_result(self, tool_call_id: str, name: str, content: str):
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": name,
            "content": content,
        })
        self._persist()

    def add_assistant_tool_call(self, content: str | None, tool_calls: list[dict] | None):
        msg = {"role": "assistant"}
        if content:
            msg["content"] = content
        if tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["name"],
                        "arguments": json.dumps(tc["arguments"]),
                    },
                }
                for tc in tool_calls
            ]
        self.messages.append(msg)
        self._persist()

    def _persist(self):
        with open(self.session_file, "w") as f:
            json.dump({"session_id": self.session_id, "messages": self.messages}, f, indent=2)

    def get_conversation_history(self) -> list[dict]:
        return [
            {"role": m["role"], "content": m["content"]}
            for m in self.messages
            if m["role"] in ("user", "assistant") and m.get("content")
        ]
