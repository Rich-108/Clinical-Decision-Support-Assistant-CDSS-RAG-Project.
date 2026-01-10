from sentence_transformers import SentenceTransformer

# Lightweight, fast, industry-standard model
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(text_chunks: list):
    """
    Convert medical text chunks into vector embeddings.
    """
    embeddings = model.encode(text_chunks)
    return embeddings
