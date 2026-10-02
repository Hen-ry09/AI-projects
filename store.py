import json
from pathlib import Path

import chromadb
from chromadb.config import Settings

EMBEDDINGS = Path("data/embeddings.json")
CHROMA_DIR = Path("data/chroma_db")


def main():
    with open(EMBEDDINGS, encoding="utf-8") as f:
        chunks = json.load(f)

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )

    collection = client.get_or_create_collection(name="ww2_germany")

    ids = [str(c["chunk_id"]) for c in chunks]
    documents = [f"{c['section']}: {c['text']}" for c in chunks]
    metadatas = [{"section": c["section"]} for c in chunks]
    embeddings = [c["embedding"] for c in chunks]

    count = collection.count()
    if count > 0:
        collection.delete(ids=collection.get()["ids"])

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    dims = len(embeddings[0]) if embeddings else 0
    print(f"Stored {len(chunks)} vectors → {CHROMA_DIR}")
    print(f"  Collection: ww2_germany, dims: {dims}")


if __name__ == "__main__":
    main()
