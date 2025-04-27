import streamlit as st
import chromadb
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.ui.pubmed_ui import PubMedUI
from app.ui.paper_qa_ui import PaperQAUIController
from app.agents import SinglePaperOrchestratorAgent
from app.agents.generate_summary_agent import GenerateSummaryAgent
from app.core.pdf_loader import load_pdf
from app.core.vector_storage import init_chroma_db
from app.core.embedding_generator import get_embeddings_model
from app.agents.orchestrator import OrchestratorAgent

def init_pdf_agent():
    """Initialize the agent for PDF processing."""
    collection = init_chroma_db()
    embeddings = get_embeddings_model()
    agent = OrchestratorAgent(collection=collection)
    return agent

def main():
    """
    Main function for the Research Paper Copilot app.
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
    if 'qa_history' not in st.session_state:
        st.session_state['qa_history'] = []
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Search Papers", "Paper Q&A", "Upload PDF & QnA"])
    
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
    
    elif page == "Upload PDF & QnA":
        # PDF Upload and Q&A functionality
        st.title("PDF Query Answering System")
        
        # File uploader widget
        uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
        
        if uploaded_file is not None:
            # Saving the uploaded file to a temporary location
            with open("temp_uploaded_file.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("File uploaded successfully!")
            
            # Initialize agents
            pdf_agent = init_pdf_agent()
            summary_agent = GenerateSummaryAgent()
            
            # Generate summary as soon as the file is uploaded
            with st.spinner("Generating summary..."):
                try:
                    # Load the PDF directly
                    documents = load_pdf("temp_uploaded_file.pdf")
                    if documents:
                        # Extract text from all documents
                        full_text = "\n\n".join([doc.page_content for doc in documents])
                        
                        # Generate summary using the summary agent directly
                        summary = summary_agent.generate_summary(
                            paper_text=full_text,
                            max_length=5000,
                            summary_type="paragraphs"
                        )
                        
                        st.subheader("Document Summary")
                        st.write(summary)
                    else:
                        st.error("No content found in the PDF. Please check the file.")
                except Exception as e:
                    st.error(f"Error generating summary: {str(e)}")
                    st.info("Please try again or proceed with Q&A.")
            
            # Text input for query
            query = st.text_input("Ask your question:")
            
            if query:
                # Using the uploaded PDF to process the query
                with st.spinner("Generating answer..."):
                    try:
                        response = pdf_agent.answer_query(query=query, filepath="temp_uploaded_file.pdf")
                        
                        # Displaying the response
                        st.subheader("Answer:")
                        st.write(response)
                        
                        # Store Q&A in session state
                        st.session_state.qa_history.append({
                            'question': query,
                            'answer': response
                        })
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
                        st.info("Please try rephrasing your question.")
            
            # Display Q&A history
            if st.session_state.qa_history:
                st.subheader("Q&A History")
                for qa in st.session_state.qa_history:
                    st.write(f"Q: {qa['question']}")
                    st.write(f"A: {qa['answer']}")
                    st.write("---")

if __name__ == "__main__":
    main() 