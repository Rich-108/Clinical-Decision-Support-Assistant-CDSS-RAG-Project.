# MUST BE AT THE VERY TOP
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from app.api.guidelines import router as guidelines_router
from app.api.search import router as search_router
from app.api.cdss import router as cdss_router
from app.services.persistence import load_index
from app.services import state

app = FastAPI(
    title="Clinical Decision Support Assistant (CDSS)",
    description="RAG-based CDSS with FAISS, multi-PDF support, and citations",
    version="1.0.0"
)

# Load persisted FAISS index + documents on startup
index, documents = load_index()
if index is not None:
    state.faiss_index = index
    state.documents = documents
    print("✅ Clinical guidelines loaded from disk")
else:
    print("⚠️ No saved clinical guidelines found")

# Register routers
app.include_router(guidelines_router)
app.include_router(search_router)
app.include_router(cdss_router)


@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": "CDSS RAG Backend"
    }
@app.get("/")
def root():
    return {
        "message": "CDSS backend is running",
        "docs": "/docs"
    }
    