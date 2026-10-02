import os
import sys
from pathlib import Path

import chromadb
import gradio as gr
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI

CHROMA_DIR = Path("data/chroma_db")
COLLECTION_NAME = "ww2_germany"

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful historian specialising in Germany's World War II history.\n"
    "Use the retrieved context below to answer the user's question.\n"
    "If the context doesn't contain enough information, say so politely.\n"
    "Cite the relevant sections when possible.\n"
)


def bootstrap():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set.")
        sys.exit(1)

    if not CHROMA_DIR.exists():
        print(f"ERROR: ChromaDB not found. Run store.py first.")
        sys.exit(1)

    chroma_client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    llm_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    return collection, llm_client


collection, llm_client = bootstrap()


def retrieve_context(query: str, top_k: int = 3) -> str:
    response = llm_client.embeddings.create(
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


def respond(message: str, history: list):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)

    context = retrieve_context(message)

    user_content = (
        f"Context from the knowledge base:\n{context}\n\n"
        f"Question: {message}"
    )
    messages.append({"role": "user", "content": user_content})

    response = llm_client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages,
    )

    return response.choices[0].message.content


with gr.Blocks() as demo:
    gr.Markdown(
        """
    # World War II History Chatbot
    Ask anything about **Nazi Germany (1933–1945)** — political events, military campaigns, the Holocaust, or the aftermath.
    Answers are retrieved from a knowledge base and cited by section.
    """
    )

    chatbot = gr.ChatInterface(
        fn=respond,
        title=None,
        description=None,
        submit_btn="Send",
    )


if __name__ == "__main__":
    demo.launch(
        theme=gr.themes.Soft(
            primary_hue="red",
            secondary_hue="neutral",
            neutral_hue="stone",
        ),
        css="""footer {display: none !important}.gradio-container {max-width: 800px !important; margin: auto;}""",
    )
