from app.retriever.pubmed.pubmed_retriever import fetch_pmc_papers
from app.retriever.pubmed.pubmed_client import fetch_pmc_full_paper
from app.retriever.pubmed.pubmed_parser import extract_text_from_pmc_xml
from typing import List, Dict, Tuple, Optional

class PubMedAgent:
    """
    Agent for retrieving and processing research papers from PubMed Central.
    """
    
    def __init__(self, top_k: int = 5):
        """
        Initialize the PubMed agent.
        
        Args:
            top_k: Maximum number of papers to retrieve
        """
        self.top_k = top_k
    
    def search_papers(self, query: str) -> List[str]:
        """
        Search for papers matching the query and return their PMC IDs.
        
        Args:
            query: Search query string
            
        Returns:
            List of PMC IDs
        """
        return fetch_pmc_papers(query, self.top_k)
    
    def get_paper_text(self, pmcid: str) -> str:
        """
        Retrieve and parse the full text of a paper by its PMC ID.
        
        Args:
            pmcid: PubMed Central ID
            
        Returns:
            Extracted text from the paper
        """
        xml_text = fetch_pmc_full_paper(pmcid)
        return extract_text_from_pmc_xml(xml_text)
    
    def search_and_retrieve(self, query: str) -> List[Dict[str, str]]:
        """
        Search for papers and retrieve their full text.
        
        Args:
            query: Search query string
            
        Returns:
            List of dictionaries containing PMC IDs and paper text
        """
        pmc_ids = self.search_papers(query)
        results = []
        
        for pmcid in pmc_ids:
            try:
                paper_text = self.get_paper_text(pmcid)
                results.append({
                    "pmcid": pmcid,
                    "text": paper_text
                })
            except Exception as e:
                print(f"Error retrieving paper {pmcid}: {str(e)}")
                
        return results
