from fastapi import APIRouter
from app.services import state
from app.services.search import semantic_search

router = APIRouter(prefix="/search", tags=["Clinical Search"])

@router.post("/")
def search_guidelines(query: str):
    if state.faiss_index is None:
        return {"error": "No guidelines indexed yet"}

    results = semantic_search(
        query=query,
        index=state.faiss_index,
        chunks=state.text_chunks
    )

    return {
        "query": query,
        "top_results": results
    }
