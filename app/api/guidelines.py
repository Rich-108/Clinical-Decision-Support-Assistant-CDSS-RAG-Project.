from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

router = APIRouter(prefix="/guidelines", tags=["Guidelines"])

# Directory to store uploaded PDFs
DATA_DIR = Path("data/guidelines")
DATA_DIR.mkdir(parents=True, exist_ok=True)


from app.services import state
from app.services.vector_service import create_index_from_pdf

@router.post("/upload")
async def upload_guideline(file: UploadFile = File(...)):
    # ... your existing save-to-disk code ...
    file_path = DATA_DIR / file.filename
    
    try:
        # Save file
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        # TRIGGER THE INDEXING (The missing step!)
        index, docs = create_index_from_pdf(file_path)
        
        # Update Global State
        state.faiss_index = index
        state.documents = docs

        return {"message": "PDF uploaded and indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")