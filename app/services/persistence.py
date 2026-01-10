import faiss
import pickle
from pathlib import Path

STORAGE_DIR = Path("storage")
INDEX_FILE = STORAGE_DIR / "faiss.index"
DOCS_FILE = STORAGE_DIR / "documents.pkl"

STORAGE_DIR.mkdir(exist_ok=True)

def save_index(index, documents):
    faiss.write_index(index, str(INDEX_FILE))
    with open(DOCS_FILE, "wb") as f:
        pickle.dump(documents, f)

def load_index():
    if INDEX_FILE.exists() and DOCS_FILE.exists():
        index = faiss.read_index(str(INDEX_FILE))
        with open(DOCS_FILE, "rb") as f:
            documents = pickle.load(f)
        return index, documents
    return None, []
