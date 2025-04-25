from chromadb import Embeddings
from app.core.vector_storage import add_embeddings_to_chroma
from chromadb.api.models import Collection
from typing import List

class ChromaStorageAgent:
    def __init__(self, collection: Collection):
        self.collection = collection

    def store_embeddings(self, documents, embeddings):
        """Store embeddings in Chroma."""
        add_embeddings_to_chroma(documents=documents, embeddings=embeddings, collection=self.collection)