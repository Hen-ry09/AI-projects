import json
import re
from pathlib import Path

import pandas as pd

DATA_SOURCE = Path("/Users/hayshay_99/Desktop/rag world war data/Germany_World_War_II_History.csv")
OUTPUT = Path("data/cleaned.json")


def clean_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def main():
    df = pd.read_csv(DATA_SOURCE)
    df = df.dropna(subset=["Section", "Content"])
    df["Section"] = df["Section"].apply(clean_text)
    df["Content"] = df["Content"].apply(clean_text)
    df = df.drop_duplicates(subset=["Section", "Content"])
    df = df.reset_index(drop=True)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    records = df.to_dict(orient="records")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"Cleaned {len(records)} records → {OUTPUT}")


if __name__ == "__main__":
    main()
