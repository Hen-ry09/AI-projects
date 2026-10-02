import os
import sys
from pathlib import Path

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI

CHROMA_DIR = Path("data/chroma_db")
COLLECTION_NAME = "ww2_germany"
MAX_HISTORY = 6

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful historian specialising in Germany's World War II history.\n"
    "Use the retrieved context below to answer the user's question.\n"
    "If the context doesn't contain enough information, say so politely.\n"
    "Cite the relevant sections when possible.\n"
)


def get_relevant_context(collection, query: str, client: OpenAI, top_k: int = 3) -> str:
    response = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input=[query],
    )
    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    lines = []
    for doc, meta in zip(documents, metadatas):
        lines.append(f"[Section: {meta['section']}] {doc}")
    return "\n\n".join(lines)


def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY environment variable is not set.")
        sys.exit(1)

    chroma_dir = CHROMA_DIR
    if not chroma_dir.exists():
        print(f"ERROR: ChromaDB not found at {chroma_dir}. Run store.py first.")
        sys.exit(1)

    chroma_client = chromadb.PersistentClient(
        path=str(chroma_dir),
        settings=Settings(anonymized_telemetry=False),
    )
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    llm_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("WWII RAG Chatbot (type 'quit' to exit)\n")

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user_input.strip().lower() in ("quit", "exit"):
            break

        if not user_input.strip():
            continue

        context = get_relevant_context(collection, user_input, llm_client)

        user_message = (
            f"Context from the knowledge base:\n{context}\n\n"
            f"Question: {user_input}"
        )
        messages.append({"role": "user", "content": user_message})

        try:
            response = llm_client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages,
            )
        except Exception as exc:
            print(f"API error: {exc}")
            continue

        reply = response.choices[0].message.content
        print(f"Bot: {reply}\n")

        messages.append({"role": "assistant", "content": reply})

        if len(messages) > MAX_HISTORY + 1:
            messages[:] = [messages[0]] + messages[-(MAX_HISTORY - 1):]


if __name__ == "__main__":
    main()
