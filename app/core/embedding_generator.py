from langchain.embeddings import HuggingFaceEmbeddings
from typing import List

def get_embeddings_model(model_name="all-MiniLM-L6-v2"):
    """Return an embeddings model from HuggingFace."""
    return HuggingFaceEmbeddings(model_name=model_name)

def generate_embeddings(documents: List[str], embeddings_model):
    """Generate embeddings for a list of documents."""
    return embeddings_model.embed_documents(documents)