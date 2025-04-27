import streamlit as st
from typing import List, Dict, Optional
from app.agents import PubMedAgent

class PubMedUI:
    """
    UI component for PubMed search and paper selection.
    """
    
    def __init__(self, top_k: int = 5):
        """
        Initialize the PubMed UI.
        
        Args:
            top_k: Maximum number of papers to retrieve
        """
        self.pubmed_agent = PubMedAgent(top_k=top_k)
        self.top_k = top_k
    
    def render_search_interface(self) -> Optional[str]:
        """
        Render the search interface and return the selected PMC ID.
        
        Returns:
            Selected PMC ID or None if no paper is selected
        """
        st.title("PubMed Research Paper Search")
        
        # Initialize selection state if not present
        if 'selected_paper_index' not in st.session_state:
            st.session_state['selected_paper_index'] = None
        
        # Search input
        query = st.text_input("Enter your search query:", 
                             placeholder="e.g., machine learning in healthcare")
        
        if not query:
            return None
        
        # Search button
        if st.button("Search"):
            with st.spinner("Searching PubMed..."):
                # Search for papers
                papers = self.pubmed_agent.search_and_retrieve(query)
                
                if not papers:
                    st.warning("No papers found for your query. Please try a different search term.")
                    return None
                
                # Store papers in session state
                st.session_state['search_results'] = papers
                st.session_state['selected_paper_index'] = None  # Reset selection on new search
        
        # Display papers if we have search results
        if 'search_results' in st.session_state and st.session_state['search_results']:
            papers = st.session_state['search_results']
            st.subheader(f"Found {len(papers)} papers:")
            
            # Display papers in a more visual way
            for i, paper in enumerate(papers):
                with st.container():
                    st.markdown(f"### Paper {i+1}: {paper['pmcid']}")
                    st.markdown(f"**Preview:** {paper['text'][:200]}...")
                    
                    # Add a button to select this paper
                    if st.button(f"Select Paper {i+1}", key=f"select_{i}"):
                        st.session_state['selected_paper_index'] = i
                        st.session_state['selected_paper'] = {
                            'pmcid': paper['pmcid'],
                            'text': paper['text']
                        }
                        st.rerun()
                    
                    st.markdown("---")
            
            # Show success message if a paper is selected
            if st.session_state['selected_paper_index'] is not None:
                selected_paper = papers[st.session_state['selected_paper_index']]
                st.success(f"Paper {selected_paper['pmcid']} selected!")
                return selected_paper['pmcid']
        
        # If we have a selected paper in session state, return its PMC ID
        if 'selected_paper' in st.session_state and st.session_state['selected_paper'] is not None:
            return st.session_state['selected_paper']['pmcid']
        
        return None
    
    def render_paper_details(self, pmcid: str) -> Dict[str, str]:
        """
        Render the paper details and return the paper data.
        
        Args:
            pmcid: PubMed Central ID
            
        Returns:
            Paper data dictionary
        """
        st.subheader(f"Paper Details ({pmcid})")
        
        # Get paper text
        paper_text = self.pubmed_agent.get_paper_text(pmcid)
        
        # Display paper text
        st.text_area("Paper Text", paper_text, height=300)
        
        # Store paper data in session state
        paper_data = {
            "pmcid": pmcid,
            "text": paper_text
        }
        st.session_state['paper_data'] = paper_data
        
        return paper_data