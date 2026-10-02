"""
Enhanced retrieval: query expansion + hybrid scoring + MMR diversity + context window.

Usage:
    from retriever import Retriever
    r = Retriever()
    results = r.retrieve("What festivals are in the Volta region?")
"""

import os
import re

import chromadb
from chromadb.errors import NotFoundError
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

CHROMA_DIR = os.path.join(os.path.dirname(__file__), ".chroma")
COLLECTION_NAME = "ghana-rag"
EXPANDED_QUERIES = 3
INITIAL_RESULTS = 15
FINAL_RESULTS = 5
CONTEXT_WINDOW = 1  # chunks before/after each result to include

EMBED_MODEL = "text-embedding-ada-002"
EMBED_URL = "https://openrouter.ai/api/v1/embeddings"


class _OpenRouterEmbedding:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def __call__(self, input: list[str]) -> list[list[float]]:
        import requests
        response = requests.post(
            EMBED_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": EMBED_MODEL, "input": input},
        )
        response.raise_for_status()
        return [d["embedding"] for d in response.json()["data"]]

    def embed_query(self, input: str | list[str]) -> list[list[float]]:
        texts = input if isinstance(input, list) else [input]
        return self(texts)

    @staticmethod
    def name() -> str:
        return "openrouter"


class Retriever:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in .env")

        self.api_key = api_key
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.embed_fn = _OpenRouterEmbedding(api_key)
        self.llm = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        try:
            self.collection = self.client.get_collection(
                COLLECTION_NAME, embedding_function=self.embed_fn
            )
        except NotFoundError:
            raise RuntimeError(
                f"Collection '{COLLECTION_NAME}' not found. Run process_rag_data.py first."
            )

    # ── Query Normalization ─────────────────────────────────────────────────

    def _normalize_query(self, query: str) -> str:
        """Fix casing for known Ghanaian ethnic groups that are also common English words."""
        known_groups = {
            "ewe": "Ewe", "ga": "Ga", "akan": "Akan", "fante": "Fante",
            "ashanti": "Ashanti", "asante": "Asante", "dagomba": "Dagomba",
            "gonja": "Gonja", "dagaaba": "Dagaaba", "frafra": "Frafra",
            "kassena": "Kassena", "mamprusi": "Mamprusi", "nanumba": "Nanumba",
            "nzema": "Nzema", "ahanta": "Ahanta", "efutu": "Effutu",
        }
        words = query.split()
        for i, w in enumerate(words):
            if w.lower() in known_groups:
                words[i] = known_groups[w.lower()]
        return " ".join(words)

    # ── Query Expansion ──────────────────────────────────────────────────────

    def _expand_query(self, query: str) -> list[str]:
        prompt = (
            f"You are a search query expansion assistant. Given a user's question about "
            f"Ghanaian culture, tourism, or languages, generate {EXPANDED_QUERIES} alternative "
            f"queries that would retrieve the most relevant information. "
            f"IMPORTANT: 'Ewe' is a major ethnic group in Ghana (not an animal). "
            f"'Ga' is an ethnic group in Ghana (not a chemical element). "
            f"Keep original spelling of ethnic groups, regions, festivals, and place names intact. "
            f"Make them diverse — different phrasings, synonyms, and related terms. "
            f"Return one query per line, no numbering, no labels.\n\n"
            f"Original query: {query}"
        )
        try:
            resp = self.llm.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300,
            )
            text = resp.choices[0].message.content or ""
            expanded = [q.strip() for q in text.split("\n") if q.strip()]
            return [query] + expanded[:EXPANDED_QUERIES]
        except Exception:
            return [query]

    # ── Vector Search ────────────────────────────────────────────────────────

    def _vector_search(self, queries: list[str], n: int) -> list[dict]:
        seen_ids: set[str] = set()
        results = []

        for q in queries:
            try:
                res = self.collection.query(query_texts=[q], n_results=n)
                if not res["documents"] or not res["documents"][0]:
                    continue
                for doc, meta, dist, idx in zip(
                    res["documents"][0],
                    res["metadatas"][0],
                    res["distances"][0] if res.get("distances") else [0] * len(res["documents"][0]),
                    res["ids"][0],
                ):
                    if idx not in seen_ids:
                        seen_ids.add(idx)
                        results.append({
                            "id": idx,
                            "text": doc,
                            "metadata": meta,
                            "score": 1.0 - dist,
                            "source": "vector",
                        })
            except Exception:
                continue

        return results

    # ── Keyword Scoring ──────────────────────────────────────────────────────

    def _keyword_score(self, text: str, query: str) -> float:
        q_words = set(re.findall(r"\w+", query.lower()))
        t_words = re.findall(r"\w+", text.lower())
        if not q_words or not t_words:
            return 0.0
        matches = sum(1 for w in t_words if w in q_words)
        return matches / len(t_words) if t_words else 0.0

    def _hybrid_rerank(self, results: list[dict], query: str) -> list[dict]:
        for r in results:
            kw_score = self._keyword_score(r["text"], query)
            r["score"] = 0.7 * r["score"] + 0.3 * kw_score
        return sorted(results, key=lambda x: x["score"], reverse=True)

    # ── MMR Re-ranking ──────────────────────────────────────────────────────

    def _mmr_rerank(self, results: list[dict], lambda_param: float = 0.6, top_n: int = FINAL_RESULTS) -> list[dict]:
        if not results:
            return []

        import numpy as np

        def _get_emb(texts: list[str]) -> list[list[float]]:
            return self.embed_fn(texts)

        texts = [r["text"] for r in results]
        embeddings = _get_emb(texts)
        emb_matrix = np.array(embeddings)

        selected = [0]
        remaining = list(range(1, len(results)))

        while len(selected) < min(top_n, len(results)):
            sim_to_query = np.array([
                1.0 - float(np.dot(emb_matrix[i], emb_matrix[0]) /
                             (np.linalg.norm(emb_matrix[i]) * np.linalg.norm(emb_matrix[0]) + 1e-10))
                for i in remaining
            ])
            sim_to_selected = np.array([
                max(float(np.dot(emb_matrix[i], emb_matrix[s]) /
                          (np.linalg.norm(emb_matrix[i]) * np.linalg.norm(emb_matrix[s]) + 1e-10))
                    for s in selected)
                for i in remaining
            ])
            mmr_scores = lambda_param * sim_to_query - (1 - lambda_param) * sim_to_selected
            best_idx = remaining[int(np.argmax(mmr_scores))]
            selected.append(best_idx)
            remaining.remove(best_idx)

        return [results[i] for i in selected]

    # ── Context Window ───────────────────────────────────────────────────────

    def _expand_context(self, results: list[dict]) -> list[dict]:
        ids = [r["id"] for r in results]
        expanded = list(results)
        for r in results:
            m = re.match(r"chunk-(\d+)", r["id"])
            if not m:
                continue
            idx = int(m.group(1))
            for offset in range(-CONTEXT_WINDOW, CONTEXT_WINDOW + 1):
                if offset == 0:
                    continue
            neighbor_id = f"chunk-{idx + offset}"
            if neighbor_id in ids:
                continue
            try:
                res = self.collection.get(ids=[neighbor_id])
                if res["documents"] and res["documents"][0]:
                    expanded.append({
                        "id": neighbor_id,
                        "text": res["documents"][0],
                        "metadata": res["metadatas"][0] if res.get("metadatas") else {},
                        "score": r["score"] * 0.9,
                        "source": "context",
                    })
                    ids.append(neighbor_id)
            except Exception:
                continue

        return expanded

    # ── Public API ──────────────────────────────────────────────────────────

    def retrieve(self, query: str, n_results: int = FINAL_RESULTS) -> list[dict]:
        query = self._normalize_query(query)
        queries = self._expand_query(query)
        results = self._vector_search(queries, n=INITIAL_RESULTS)
        results = self._hybrid_rerank(results, query)
        results = self._mmr_rerank(results, top_n=INITIAL_RESULTS)
        results = self._expand_context(results)
        results = sorted(results, key=lambda x: x["score"], reverse=True)[:n_results]
        return results

    def retrieve_text(self, query: str, n_results: int = FINAL_RESULTS) -> str:
        results = self.retrieve(query, n_results=n_results)
        if not results:
            return ""
        parts = []
        for i, r in enumerate(results, 1):
            parts.append(f"[{i}] (score: {r['score']:.3f})\n{r['text']}")
        return "\n\n".join(parts)
