from app.core.embedding_generator import get_embeddings_model
from app.core.vector_storage import query_chroma
from chromadb.api.models.Collection import Collection
from typing import Tuple, List
from langchain.schema import Document


embed_model = get_embeddings_model()

def retrieve_relevant_documents(query: str, collection: Collection, top_k: int = 5) -> Tuple[List[Document], List[dict]]:
    """Return top_k documents and metadata from Chroma for a query."""
    docs, metas = query_chroma(query=query, collection=collection, embed_query_fn=embed_model, top_k = top_k)

    return docs, metas