from app.core.embedding_generator import generate_embeddings, get_embeddings_model
from typing import List

class EmbeddingGenerationAgent:
    def __init__(self):
        self.embeddings_model = get_embeddings_model()  # Default model, can be passed as argument

    def generate_embeddings(self, documents):
        """Generate embeddings for a list of documents."""
        if isinstance(documents[0], str):  # If it's a list of strings
            texts = documents  # Directly use the list of strings
        else:  # If it's a list of 'Document' objects
            texts = [doc.page_content for doc in documents]
        return generate_embeddings(documents=texts, embeddings_model=self.embeddings_model)