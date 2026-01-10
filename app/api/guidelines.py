from fastapi import APIRouter, UploadFile, File
from pathlib import Path

from app.services.pdf_loader import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.services.embeddings import create_embeddings
from app.services.vector_store import build_faiss_index
from app.services.persistence import save_index
from app.services import state

router = APIRouter(
    prefix="/guidelines",
    tags=["Clinical Guidelines"]
)

# Folder to store uploaded PDFs
DATA_DIR = Path("data/guidelines")
DATA_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_guideline(file: UploadFile = File(...)):
    """
    Upload a clinical guideline PDF.
    Supports MULTIPLE PDFs.
    Persists FAISS index + document metadata.
    """

    # 1️⃣ Save PDF to disk
    file_path = DATA_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2️⃣ Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    # 3️⃣ Chunk text (medical-safe)
    chunks = chunk_text(extracted_text)

    # 4️⃣ Convert chunks → document records (text + source)
    new_documents = []
    for chunk in chunks:
        new_documents.append({
            "text": chunk,
            "source": file.filename
        })

    # 5️⃣ Append to GLOBAL state (multi-PDF support)
    state.documents.extend(new_documents)

    # 6️⃣ Rebuild embeddings for ALL documents
    all_texts = [doc["text"] for doc in state.documents]
    embeddings = create_embeddings(all_texts)

    # 7️⃣ Build FAISS index
    index = build_faiss_index(embeddings)
    state.faiss_index = index

    # 8️⃣ Persist index + metadata to disk
    save_index(index, state.documents)

    # 9️⃣ Return clear response
    return {
        "uploaded_file": file.filename,
        "total_documents": len(state.documents),
        "total_vectors": index.ntotal
    }
