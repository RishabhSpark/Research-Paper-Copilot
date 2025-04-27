from typing import Optional
from .response_generation_agent import ResponseGenerationAgent

class GenerateSummaryAgent:
    """
    Agent for generating summaries of research papers.
    """
    
    def __init__(self):
        """
        Initialize the summary generation agent.
        """
        self.response_agent = ResponseGenerationAgent()
    
    def generate_summary(self, paper_text: str, max_length: int = 5000, summary_type: str = "paragraphs") -> str:
        """
        Generate a summary of a paper.
        
        Args:
            paper_text: Text of the paper
            max_length: Maximum length of text to summarize (default: 5000)
            summary_type: Type of summary - "paragraphs" or "sentences" (default: "paragraphs")
            
        Returns:
            Generated summary
        """
        # Truncate text if needed
        truncated_text = paper_text[:max_length] + "..." if len(paper_text) > max_length else paper_text
        
        # Create appropriate prompt based on summary type
        if summary_type == "paragraphs":
            summary_prompt = f"Summarize the following research paper in 3-5 paragraphs:\n\n{truncated_text}"
        else:  # sentences
            summary_prompt = f"Summarize the following research paper in 3-5 sentences:\n\n{truncated_text}"
        
        # Generate summary using response agent
        summary = self.response_agent.generate_response(prompt=summary_prompt)
        
        return summary 