from app.core.pdf_loader import load_pdf
from langchain.schema import Document
from typing import List

class PDFLoaderAgent:
    def __init__(self):
        pass

    def load_pdf(self, filepath: str) -> List[Document]:
        """Load PDF into documents."""
        return load_pdf(filepath)