import streamlit as st
import chromadb
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.ui.pubmed_ui import PubMedUI
from app.ui.paper_qa_ui import PaperQAUIController
from app.agents import SinglePaperOrchestratorAgent

def main():
    """
    Main function for the PubMed research paper Q&A app.
    """
    # Set page config
    st.set_page_config(
        page_title="Research Paper Copilot",
        layout="wide"
    )
    
    # Initialize ChromaDB with persistent storage
    try:
        # Create a persistent client with a specific path
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection("pubmed_papers")
    except Exception as e:
        st.error(f"Error initializing ChromaDB: {str(e)}")
        st.info("Using in-memory ChromaDB as fallback")
        # Fallback to in-memory client
        client = chromadb.Client()
        collection = client.create_collection("pubmed_papers")
    
    # Initialize UI components
    pubmed_ui = PubMedUI(top_k=5)
    orchestrator = SinglePaperOrchestratorAgent(collection=collection)
    qa_controller = PaperQAUIController(orchestrator=orchestrator)
    
    # Initialize session state
    if 'selected_paper' not in st.session_state:
        st.session_state['selected_paper'] = None
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Search Papers"
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Search Papers", "Paper Q&A"])
    
    # Update current page in session state
    st.session_state['current_page'] = page
    
    # Render the appropriate page
    if page == "Search Papers":
        # Render the search interface
        pubmed_ui.render_search_interface()
    
    elif page == "Paper Q&A":
        # Check if a paper is selected
        if st.session_state['selected_paper'] is None:
            st.warning("No paper selected. Please go to the 'Search Papers' page to select a paper.")
            return
        
        # Get the paper data
        paper_data = st.session_state['selected_paper']
        
        # Render the Q&A interface
        qa_controller.render_qa_interface(paper_data)

if __name__ == "__main__":
    main() 