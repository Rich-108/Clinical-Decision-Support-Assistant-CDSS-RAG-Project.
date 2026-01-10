from fastapi import APIRouter, Query, HTTPException
from app.services import state
from app.services.search import semantic_search
from app.services.generator import generate_answer

router = APIRouter(
    prefix="/cdss",
    tags=["Clinical Decision Support"]
)


@router.post("/ask")
def ask_cdss(query: str = Query(..., min_length=5)):
    """
    Ask a clinical question.
    Retrieves evidence from indexed guidelines and generates an answer.
    """

    if state.faiss_index is None or not state.documents:
        raise HTTPException(
            status_code=400,
            detail="No clinical guidelines indexed"
        )

    # 🔍 Retrieve evidence (Phase-2 compliant)
    evidence = semantic_search(
        query=query,
        index=state.faiss_index,
        documents=state.documents,
        top_k=3
    )

    if not evidence:
        return {
            "question": query,
            "answer": "No relevant clinical evidence found.",
            "citations": [],
            "evidence_used": []
        }

    # 🤖 Generate answer using LLM
    answer = generate_answer(query, evidence)

    citations = list({e["source"] for e in evidence})

    return {
        "question": query,
        "answer": answer,
        "citations": citations,
        "evidence_used": evidence
    }
