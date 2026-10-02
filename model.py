import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY is not set in .env")
    sys.exit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def chat(prompt: str, system_prompt: str | None = None) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content
