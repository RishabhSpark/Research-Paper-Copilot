from app.retriever.document_retriever import retrieve_relevant_documents
from chromadb.api.models import Collection
from typing import List, Tuple

class DocumentRetrievalAgent:
    def __init__(self, collection: Collection, top_k: int = 5):
        self.collection = collection
        self.top_k = top_k

    def retrieve_documents(self, query: str) -> Tuple[List[str], List[dict]]:
        """Retrieve relevant documents and their metadata."""
        docs, metas = retrieve_relevant_documents(query, self.collection, self.top_k)
        return docs, metas