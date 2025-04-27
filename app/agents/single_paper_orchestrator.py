from .embeddings_generation_agent import EmbeddingGenerationAgent
from .chroma_storage_agent import ChromaStorageAgent
from .text_chunking_agent import TextChunkingAgent
from .prompt_builder_agent import PromptBuilderAgent
from .response_generation_agent import ResponseGenerationAgent
from chromadb.api.models import Collection
from typing import List, Dict, Optional
from langchain.schema import Document

class SinglePaperOrchestratorAgent:
    """
    Orchestrator for processing a single paper for Q&A.
    """
    
    def __init__(self, collection: Collection):
        """
        Initialize the single paper orchestrator.
        
        Args:
            collection: ChromaDB collection for storing embeddings
        """
        self.embeddings_generation_agent = EmbeddingGenerationAgent()
        self.chromadb_storage_agent = ChromaStorageAgent(collection=collection)
        self.chunking_agent = TextChunkingAgent()
        self.prompt_builder_agent = PromptBuilderAgent()
        self.response_agent = ResponseGenerationAgent()
        self.collection = collection
    
    def process_paper(self, paper_text: str) -> List[Document]:
        """
        Process a single paper by chunking it and generating embeddings.
        
        Args:
            paper_text: Text of the paper
            
        Returns:
            List of chunked documents
        """
        # Convert paper text to Document objects
        doc = Document(page_content=paper_text, metadata={"source": "pubmed"})
        
        # Chunk the document
        chunked_docs = self.chunking_agent.chunk_documents([doc])
        
        # Generate embeddings for chunked documents
        embeddings = self.embeddings_generation_agent.generate_embeddings(chunked_docs)
        
        # Store embeddings in ChromaDB
        self.chromadb_storage_agent.store_embeddings(chunked_docs, embeddings)
        
        return chunked_docs
    
    def answer_query(self, query: str, paper_text: str) -> str:
        """
        Answer a query based on a single paper.
        
        Args:
            query: User query
            paper_text: Text of the paper
            
        Returns:
            Generated response
        """
        # Process the paper
        chunked_docs = self.process_paper(paper_text)
        
        # Build prompt and generate response
        context = [doc.page_content for doc in chunked_docs]
        prompt = self.prompt_builder_agent.build_prompt(query=query, docs=context)
        response = self.response_agent.generate_response(prompt=prompt)
        
        return response
    
    def generate_summary(self, paper_text: str) -> str:
        """
        Generate a summary of a paper.
        
        Args:
            paper_text: Text of the paper
            
        Returns:
            Generated summary
        """
        # Generate a summary for the paper
        summary_prompt = f"Summarize the following research paper in 3-5 paragraphs:\n\n{paper_text[:5000]}..."
        summary = self.response_agent.generate_response(prompt=summary_prompt)
        
        return summary 