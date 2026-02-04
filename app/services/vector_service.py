import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Use a tiny model for 4GB RAM
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_index_from_pdf(file_path):
    # 1. Load and Split
    loader = PyPDFLoader(str(file_path))
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    
    # 2. Extract text and create Embeddings
    texts = [c.page_content for c in chunks]
    embeddings = model.encode(texts)
    
    # 3. Create FAISS Index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # 4. Prepare metadata for citations
    metadata = [{"text": c.page_content, "source": c.metadata.get("source", "Unknown")} for c in chunks]
    
    return index, metadata