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
print("🔍 Loading index...")
index, documents = load_index()
print("🔍 Index loaded result:", "Success" if index is not None else "None")
if index is not None:
    state.faiss_index = index
    state.documents = documents
    print("✅ Clinical guidelines loaded from disk")
else:
    print("⚠️ No saved clinical guidelines found")

print("🔍 Registering routers...")
# Register routers
app.include_router(guidelines_router)
print("🔍 Guidelines router registered")
app.include_router(search_router)
print("🔍 Search router registered")
app.include_router(cdss_router)
print("🔍 CDSS router registered")


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
    