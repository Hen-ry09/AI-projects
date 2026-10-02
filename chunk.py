import json
from pathlib import Path

CLEANED = Path("data/cleaned.json")
OUTPUT = Path("data/chunks.json")
CHUNK_SIZE = 300
OVERLAP = 50


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_text_str = " ".join(words[start:end])
        chunks.append(chunk_text_str)
        start += chunk_size - overlap
    return chunks


def main():
    with open(CLEANED, encoding="utf-8") as f:
        records = json.load(f)

    all_chunks = []
    chunk_id = 0
    for record in records:
        section = record["Section"]
        content = record["Content"]
        chunks = chunk_text(content, CHUNK_SIZE, OVERLAP)
        for chunk_text_str in chunks:
            all_chunks.append({
                "chunk_id": chunk_id,
                "section": section,
                "text": chunk_text_str,
            })
            chunk_id += 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Created {len(all_chunks)} chunks → {OUTPUT}")


if __name__ == "__main__":
    main()
