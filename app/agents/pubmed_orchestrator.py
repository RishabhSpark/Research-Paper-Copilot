from .pubmed_agent import PubMedAgent
from .embeddings_generation_agent import EmbeddingGenerationAgent
from .chroma_storage_agent import ChromaStorageAgent
from .text_chunking_agent import TextChunkingAgent
from .prompt_builder_agent import PromptBuilderAgent
from .response_generation_agent import ResponseGenerationAgent
from chromadb.api.models import Collection
from typing import List, Dict

class PubMedOrchestratorAgent:
    """
    Orchestrator for PubMed agent that coordinates the retrieval, processing, and response generation
    for research papers from PubMed Central.
    """
    
    def __init__(self, collection: Collection, top_k: int = 5):
        """
        Initialize the PubMed orchestrator.
        
        Args:
            collection: ChromaDB collection for storing embeddings
            top_k: Maximum number of papers to retrieve
        """
        self.pubmed_agent = PubMedAgent(top_k=top_k)
        self.embeddings_generation_agent = EmbeddingGenerationAgent()
        self.chromadb_storage_agent = ChromaStorageAgent(collection=collection)
        self.chunking_agent = TextChunkingAgent()
        self.prompt_builder_agent = PromptBuilderAgent()
        self.response_agent = ResponseGenerationAgent()
        self.collection = collection
    
    def process_papers(self, papers: List[Dict[str, str]]) -> List[str]:
        """
        Process papers by chunking them and generating embeddings.
        
        Args:
            papers: List of dictionaries containing PMC IDs and paper text
            
        Returns:
            List of chunked documents
        """
        # Extract paper texts
        paper_texts = [paper["text"] for paper in papers]
        
        # Chunk the documents
        chunked_docs = self.chunking_agent.chunk_documents(paper_texts)
        
        # Generate embeddings for chunked documents
        embeddings = self.embeddings_generation_agent.generate_embeddings(chunked_docs)
        
        # Store embeddings in ChromaDB
        self.chromadb_storage_agent.store_embeddings(chunked_docs, embeddings)
        
        return chunked_docs
    
    def answer_query(self, query: str, top_k: int = 5) -> str:
        """
        Orchestrates the agents to answer the query based on PubMed papers.
        
        Args:
            query: User query
            top_k: Maximum number of papers to retrieve
            
        Returns:
            Generated response
        """
        # Step 1: Search for papers and retrieve their text
        papers = self.pubmed_agent.search_and_retrieve(query)
        if not papers:
            return "No relevant papers found for your query. Please try a different search term."
        print(f"Retrieved {len(papers)} papers from PubMed")
        
        # Step 2: Process the papers (chunk, embed, store)
        chunked_docs = self.process_papers(papers)
        print("Processed papers (chunked, embedded, stored)")
        
        # Step 3: Build prompt and generate response
        context = [doc.page_content for doc in chunked_docs]
        prompt = self.prompt_builder_agent.build_prompt(query=query, docs=context)
        response = self.response_agent.generate_response(prompt=prompt)
        print("Response generated")
        
        return response
    
    def search_and_summarize(self, query: str, top_k: int = 5) -> Dict[str, str]:
        """
        Search for papers and provide a summary of each.
        
        Args:
            query: Search query
            top_k: Maximum number of papers to retrieve
            
        Returns:
            Dictionary with PMC IDs as keys and summaries as values
        """
        # Search for papers
        papers = self.pubmed_agent.search_and_retrieve(query)
        if not papers:
            return {"error": "No relevant papers found for your query. Please try a different search term."}
        
        summaries = {}
        for paper in papers:
            pmcid = paper["pmcid"]
            text = paper["text"]
            
            # Generate a summary for each paper
            summary_prompt = f"Summarize the following research paper in 3-5 sentences:\n\n{text[:2000]}..."
            summary = self.response_agent.generate_response(prompt=summary_prompt)
            
            summaries[pmcid] = summary
        
        return summaries
