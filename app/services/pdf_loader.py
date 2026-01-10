import fitz  # PyMuPDF
from pathlib import Path

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extracts clean text from a medical guideline PDF.
    """
    text = []
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text.append(page_text)
        doc.close()
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

    return "\n".join(text)
