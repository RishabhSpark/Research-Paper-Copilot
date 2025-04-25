from langchain_community.document_loaders import PyMuPDFLoader
from typing import List
from langchain.schema import Document
import os

def load_pdf(filepath: str) -> List[Document]:
    """Loads PDF from the given filepath and returns a list of Langchain Document objects.

    Args:
        filepath (str): PDF path

    Returns:
        List[Document]: List of langchain document objects
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"PDF not found at {filepath}")

    if not filepath.lower().endswith(".pdf"):
        raise ValueError(f"Invalid file type: '{filepath}'. Only PDF files are supported.")

    loader = PyMuPDFLoader(filepath)
    raw_documents = loader.load()

    documents = []
    for doc in raw_documents:
        cleaned_content = doc.page_content.strip()  # Basic cleaning

        metadata = {
            "source": filepath,
            "total_pages": len(raw_documents),
            "author": doc.metadata.get("author", "Unknown"),
            "creationDate": doc.metadata.get("creationDate", "Unknown"),
            "format": doc.metadata.get("format", "Unknown"),
        }

        documents.append(Document(page_content=cleaned_content, metadata=metadata))

    print(f"[PDF LOADER] Loaded {len(documents)} page(s) from '{filepath}'")
    return documents