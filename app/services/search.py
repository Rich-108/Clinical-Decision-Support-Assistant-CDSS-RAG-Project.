import numpy as np
from app.services.embeddings import model

def semantic_search(query, index, documents, top_k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(
        np.array(query_embedding), top_k
    )

    results = []
    for idx in indices[0]:
        results.append({
            "text": documents[idx]["text"],
            "source": documents[idx]["source"]
        })

    return results
