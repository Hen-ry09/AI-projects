import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

CHUNKS = Path("data/chunks.json")
OUTPUT = Path("data/embeddings.json")

load_dotenv()


def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set")
        sys.exit(1)

    with open(CHUNKS, encoding="utf-8") as f:
        chunks = json.load(f)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    texts = [c["text"] for c in chunks]

    all_embeddings = []
    batch_size = 20
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = client.embeddings.create(
            model="openai/text-embedding-3-small",
            input=batch,
        )
        all_embeddings.extend([e.embedding for e in response.data])
        print(f"  Embedded {min(i + batch_size, len(texts))}/{len(texts)}")

    for chunk, emb in zip(chunks, all_embeddings):
        chunk["embedding"] = emb

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Embedded {len(chunks)} chunks → {OUTPUT}")


if __name__ == "__main__":
    main()
