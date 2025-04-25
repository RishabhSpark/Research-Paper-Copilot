from app.core.text_splitter import chunk_documents
from langchain.schema import Document
from typing import List

class TextChunkingAgent:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Chunk documents into smaller parts."""
        return chunk_documents(
            documents=documents,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
    
