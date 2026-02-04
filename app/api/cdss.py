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
    if state.faiss_index is None or not state.documents:
        raise HTTPException(
            status_code=400,
            detail="No clinical guidelines indexed. Please upload a PDF first."
        )

    try:
        # 1. Search for chunks
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

        # 2. Call the generator with a try-except block
        try:
            answer = generate_answer(query, evidence)
        except Exception as llm_err:
            print(f"LLM Error: {llm_err}")
            raise HTTPException(
                status_code=502, 
                detail="Ollama/Phi-3 failed to generate a response. Is Ollama running?"
            )

        citations = list({e.get("source", "Unknown") for e in evidence})

        return {
            "question": query,
            "answer": answer,
            "citations": citations,
            "evidence_used": evidence
        }

    except Exception as e:
        # This catches anything else and tells you what it is
        print(f"General Error in /ask: {e}")
        raise HTTPException(status_code=500, detail=str(e))