import glob
import os
import re

import chromadb
from chromadb.errors import NotFoundError
import requests

from dotenv import load_dotenv

load_dotenv()

SKILL_DIR = os.path.join(os.path.dirname(__file__), "myskill")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), ".chroma")
COLLECTION_NAME = "ghana-skill"

EMBED_MODEL = "text-embedding-ada-002"
EMBED_URL = "https://openrouter.ai/api/v1/embeddings"


class _OpenRouterEmbedding:
    def __init__(self, api_key: str):
        self.api_key = api_key

    @staticmethod
    def name() -> str:
        return "openrouter"

    def _embed(self, input: list[str]) -> list[list[float]]:
        response = requests.post(
            EMBED_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": EMBED_MODEL, "input": input},
        )
        response.raise_for_status()
        return [d["embedding"] for d in response.json()["data"]]

    def __call__(self, input: list[str]) -> list[list[float]]:
        return self._embed(input)

    def embed_documents(self, input: list[str]) -> list[list[float]]:
        return self._embed(input)

    def embed_query(self, input: str | list[str]) -> list[list[float]]:
        texts = input if isinstance(input, list) else [input]
        return self._embed(texts)


class KnowledgeBase:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for embeddings")
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.embed_fn = _OpenRouterEmbedding(api_key)
        self.collection = self._load_or_create()

    def _load_or_create(self):
        try:
            return self.client.get_collection(
                COLLECTION_NAME, embedding_function=self.embed_fn
            )
        except NotFoundError:
            collection = self.client.create_collection(
                COLLECTION_NAME, embedding_function=self.embed_fn
            )
            self._index_knowledge(collection)
            return collection

    def _knowledge_file(self):
        kb_files = [
            f for f in glob.glob(os.path.join(SKILL_DIR, "*.md"))
            if not f.endswith("system-prompt.md")
        ]
        if not kb_files:
            return None
        with open(kb_files[0]) as f:
            return f.read()

    def _chunk(self, text: str):
        if text.startswith("---"):
            end = text.find("---", 3)
            if end != -1:
                text = text[end + 3:].strip()

        chunks = []
        section = "General"
        lines = []

        for line in text.split("\n"):
            m = re.match(r"^##\s+(.+)", line)
            if m:
                if lines:
                    chunks.append((section, "\n".join(lines).strip()))
                section = m.group(1).strip()
                lines = [line]
            else:
                lines.append(line)

        if lines:
            chunks.append((section, "\n".join(lines).strip()))
        return chunks

    def _index_knowledge(self, collection):
        content = self._knowledge_file()
        if not content:
            print("No knowledge file found to index")
            return

        chunks = self._chunk(content)
        collection.add(
            documents=[c[1] for c in chunks],
            metadatas=[{"section": c[0]} for c in chunks],
            ids=[f"chunk-{i}" for i in range(len(chunks))],
        )
        print(f"Indexed {len(chunks)} chunks into vector store")

    def search(self, query: str, n_results: int = 3) -> str:
        results = self.collection.query(
            query_texts=[query], n_results=n_results
        )
        if not results["documents"] or not results["documents"][0]:
            return ""

        parts = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            parts.append(f"[{meta['section']}]\n{doc}")

        return "\n\n".join(parts)
