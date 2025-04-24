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
    documents = loader.load()

    print(f"[PDF LOADER] Loaded {len(documents)} page(s) from '{filepath}'")
    return documents