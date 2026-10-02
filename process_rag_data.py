"""
Pipeline: Load dirty CSVs → Clean → Chunk with overlap → Embed → Store in ChromaDB.

Usage:
    python process_rag_data.py
"""

import glob
import os
import re

import pandas as pd
import requests

from chromadb import PersistentClient
from chromadb.errors import NotFoundError
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "/Users/hayshay_99/Desktop/rag data"
CHROMA_DIR = os.path.join(os.path.dirname(__file__), ".chroma")
COLLECTION_NAME = "ghana-rag"

EMBED_MODEL = "text-embedding-ada-002"
EMBED_URL = "https://openrouter.ai/api/v1/embeddings"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# ─── Cleaning ────────────────────────────────────────────────────────────────


def strip_html(text: object) -> str:
    if pd.isna(text) or text is None:
        return ""
    return re.sub(r"<[^>]+>", "", str(text)).strip()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def fix_encoding(text: str) -> str:
    text = text.encode("latin-1", errors="replace").decode("utf-8", errors="replace")
    text = text.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
    replacements = {
        "Ã©": "é", "Ã¨": "è", "Ãª": "ê", "Ã«": "ë",
        "Ã¡": "á", "Ã¢": "â", "Ã¤": "ä", "Ã£": "ã",
        "Ã²": "ò", "Ã³": "ó", "Ã´": "ô", "Ã¶": "ö",
        "Ã¹": "ù", "Ãº": "ú", "Ã»": "û", "Ã¼": "ü",
        "Ã±": "ñ", "Ã§": "ç", "Ã": "à",
        "Â ": "", "â€™": "'", "â€œ": '"', "â€": '"',
        "â€“": "–", "â€”": "—", "Â": "",
        "Å": "", "Ã": "à", "ã©": "é",
    }
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    return text


def normalize_case(text: str) -> str:
    return text.lower().strip()


def clean_value(val: object) -> str:
    text = strip_html(val)
    text = fix_encoding(text)
    text = normalize_whitespace(text)
    return text


NULLISH = {"", "nan", "n/a", "na", "none", "null", "-", "--", "??", "?", "n/a", "n/ a",
           "unknown", "unk", "nul", "na ", " ", "", "0", "no", "false", "true",
           "null ", "na ", "n/a ", "n /a", "n / a"}


def is_nullish(val: object) -> bool:
    if pd.isna(val) or val is None:
        return True
    return normalize_case(str(val)) in NULLISH


def safe(val: object) -> str:
    if is_nullish(val):
        return ""
    return clean_value(val)


def normalize_region(region: str) -> str:
    m = re.search(r"(Upper\s*(East|West)|(Greater\s*)?Accra|Central|Western|Eastern|"
                  r"Volta|Ashanti|Bono|Ahafo|Northern|North\s*East|Oti|Savannah|"
                  r"Upper\s*East|Upper\s*West|Bono\s*East|Western\s*North)", region, re.I)
    return m.group(1).title() if m else region


def clean_festivals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    for col in df.columns:
        df[col] = df[col].apply(clean_value)

    df["festival_name"] = df["festival_name"].str.strip().str.title()
    df["ethnic_group"] = df["ethnic_group"].apply(safe)
    df["region"] = df["region"].apply(safe).apply(normalize_region)
    df["typical_timing"] = df["typical_timing"].apply(safe)
    df["description"] = df["description"].apply(safe)

    df = df[df["festival_name"] != ""]
    df = df.drop_duplicates(subset=["festival_name", "ethnic_group", "region", "description"])
    return df


def clean_languages(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    for col in df.columns:
        df[col] = df[col].apply(clean_value)

    df["language_name"] = df["language_name"].str.strip().str.title()
    df["language_family"] = df["language_family"].apply(safe)
    df["primary_regions"] = df["primary_regions"].apply(safe).apply(normalize_region)
    df["estimated_speakers"] = df["estimated_speakers"].apply(safe)
    df["status"] = df["status"].apply(safe).str.capitalize()
    df["notes"] = df["notes"].apply(safe)

    df = df[df["language_name"] != ""]
    df = df.drop_duplicates(subset=["language_name", "primary_regions"])
    return df


def clean_tourism(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    for col in df.columns:
        df[col] = df[col].apply(clean_value)

    df["site_name"] = df["site_name"].str.strip().str.title()
    df["region"] = df["region"].apply(safe).apply(normalize_region)
    df["category"] = df["category"].apply(safe)
    df["description"] = df["description"].apply(safe)
    df["review_text"] = df["review_text"].apply(safe)
    df["is_unesco_site"] = (
        df["is_unesco_site"]
        .apply(safe)
        .str.lower()
        .map({"yes": "Yes", "y": "Yes", "true": "Yes", "1": "Yes", "no": "No", "n": "No", "false": "No", "0": "No", "": "Unknown"})
        .fillna("Unknown")
    )
    df["entry_fee"] = df["entry_fee"].apply(
        lambda x: "GHS 40" if x and "40" in str(x) and x not in ("", "none", "na", "n/a") else ("" if is_nullish(x) else clean_value(x))
    )

    df = df[df["site_name"] != ""]
    df = df.drop_duplicates(subset=["site_name", "region", "description"])
    return df


# ─── Load & Clean ────────────────────────────────────────────────────────────


def load_and_clean_all() -> dict[str, pd.DataFrame]:
    files = glob.glob(os.path.join(DATA_DIR, "*_dirty.csv"))
    cleaned = {}
    for fpath in files:
        name = os.path.basename(fpath)
        df = pd.read_csv(fpath, encoding="utf-8", engine="python", on_bad_lines="skip")
        print(f"  {name}: {len(df)} rows loaded")

        if "festival" in name.lower():
            df = clean_festivals(df)
        elif "language" in name.lower():
            df = clean_languages(df)
        elif "tourism" in name.lower():
            df = clean_tourism(df)

        cleaned[name] = df
        print(f"           {len(df)} rows after cleaning")
    return cleaned


# ─── Chunking with Overlap ───────────────────────────────────────────────────


def row_to_text(row: pd.Series, source: str) -> str:
    parts = [f"[Source: {source}]"]
    for col, val in row.items():
        if val and col not in ("record_id", "year_recorded", "attendance_estimate",
                                "cancelled_due_to_covid", "durbar_notes", "data_source",
                                "is_official_language", "data_source", "record_year",
                                "visit_date", "distance_from_accra_km", "opening_hours"):
            parts.append(f"{col.replace('_', ' ').title()}: {val}")
    return "\n".join(parts)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
        if start >= len(words):
            break
    return chunks


def build_chunks(cleaned: dict[str, pd.DataFrame]) -> list[str]:
    all_chunks = []
    for fname, df in cleaned.items():
        source = fname.replace("_dirty.csv", "").replace("_", " ").title()
        for _, row in df.iterrows():
            text = row_to_text(row, source)
            if not text.strip():
                continue
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
    return all_chunks


# ─── Embedding ───────────────────────────────────────────────────────────────


class OpenRouterEmbedder:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def __call__(self, input: list[str]) -> list[list[float]]:
        response = requests.post(
            EMBED_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": EMBED_MODEL, "input": input},
        )
        response.raise_for_status()
        return [d["embedding"] for d in response.json()["data"]]

    def name(self) -> str:
        return "openrouter"

    def embed_query(self, input: str | list[str]) -> list[list[float]]:
        texts = input if isinstance(input, list) else [input]
        return self(texts)


# ─── Store in ChromaDB ───────────────────────────────────────────────────────


def store_chunks(chunks: list[str], embed_fn: OpenRouterEmbedder) -> None:
    client = PersistentClient(path=CHROMA_DIR)

    try:
        collection = client.get_collection(COLLECTION_NAME, embedding_function=embed_fn)
        print(f"Collection '{COLLECTION_NAME}' already exists — dropping and rebuilding.")
        client.delete_collection(COLLECTION_NAME)
    except NotFoundError:
        pass

    collection = client.create_collection(COLLECTION_NAME, embedding_function=embed_fn)
    batch_size = 50
    total = len(chunks)

    for i in range(0, total, batch_size):
        batch = chunks[i : i + batch_size]
        collection.add(
            documents=batch,
            ids=[f"chunk-{j}" for j in range(i, min(i + batch_size, total))],
            metadatas=[{"index": j} for j in range(i, min(i + batch_size, total))],
        )
        print(f"  Stored {min(i + batch_size, total)} / {total} chunks")

    print(f"\nDone — {total} chunks stored in collection '{COLLECTION_NAME}'")


# ─── Main ────────────────────────────────────────────────────────────────────


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in .env")

    print("=" * 50)
    print("Step 1: Loading & Cleaning CSVs")
    print("=" * 50)
    cleaned = load_and_clean_all()

    print("\n" + "=" * 50)
    print("Step 2: Chunking with overlap")
    print(f"       Chunk size: {CHUNK_SIZE} words, Overlap: {CHUNK_OVERLAP} words")
    print("=" * 50)
    chunks = build_chunks(cleaned)
    print(f"  Total chunks: {len(chunks)}")

    print("\n" + "=" * 50)
    print("Step 3: Embedding & Storing in ChromaDB")
    print("=" * 50)
    embed_fn = OpenRouterEmbedder(api_key)
    store_chunks(chunks, embed_fn)

    print("\n" + "=" * 50)
    print("Sample chunks:")
    for c in chunks[:2]:
        print(f"\n---\n{c[:300]}...")


if __name__ == "__main__":
    main()
