import streamlit as st
from typing import Dict, List, Optional
from langchain.schema import Document
from app.agents import SinglePaperOrchestratorAgent
from chromadb.api.models import Collection

class PaperQAUIController:
    """
    Controller for the paper Q&A interface.
    """
    
    def __init__(self, orchestrator):
        """
        Initialize the Q&A controller.
        
        Args:
            orchestrator: SinglePaperOrchestratorAgent instance
        """
        self.orchestrator = orchestrator
        
    def render_qa_interface(self, paper_data: Dict[str, str]):
        """
        Render the Q&A interface for a paper.
        
        Args:
            paper_data: Dictionary containing paper data with 'pmcid' and 'text' keys
        """
        st.title("Paper Q&A")
        
        # Display paper info
        st.subheader(f"Paper: {paper_data['pmcid']}")
        
        # Generate and display summary
        with st.spinner("Generating summary..."):
            summary = self.orchestrator.generate_summary(paper_data['text'])
            st.subheader("Summary")
            st.write(summary)
        
        # Q&A section
        st.subheader("Ask Questions")
        query = st.text_input("Enter your question about the paper:")
        
        if query:
            with st.spinner("Generating answer..."):
                response = self.orchestrator.answer_query(query, paper_data['text'])
                st.subheader("Answer")
                st.write(response)
                
                # Store Q&A in session state
                if 'qa_history' not in st.session_state:
                    st.session_state.qa_history = []
                st.session_state.qa_history.append({
                    'question': query,
                    'answer': response
                })
        
        # Display Q&A history
        if 'qa_history' in st.session_state and st.session_state.qa_history:
            st.subheader("Q&A History")
            for qa in st.session_state.qa_history:
                st.write(f"Q: {qa['question']}")
                st.write(f"A: {qa['answer']}")
                st.write("---") 