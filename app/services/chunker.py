import re
from typing import List

def clean_text(text: str) -> str:
    # Normalize whitespace but keep structure
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 450,
    overlap: int = 100
) -> List[str]:
    """
    Medical-safe chunking with overlap.
    Word-based to preserve dosage and conditions.
    """
    text = clean_text(text)
    words = text.split(" ")

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

    return chunks
