import json
from openai import OpenAI

from .settings import Settings


class LLMClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            default_headers={
                "HTTP-Referer": "https://github.com/akwaaba-ai",
                "X-Title": "Akwaaba AI",
            },
        )

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> tuple[str, list[dict] | None]:
        kwargs = {
            "model": self.settings.openai_model,
            "messages": messages,
            "temperature": self.settings.openai_temperature,
            "max_tokens": self.settings.openai_max_tokens,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message

        tool_calls = None
        if message.tool_calls:
            tool_calls = []
            for tc in message.tool_calls:
                args = json.loads(tc.function.arguments)
                tool_calls.append({
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": args,
                })

        content = message.content or ""
        return content, tool_calls
