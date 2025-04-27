import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.agents.orchestrator import OrchestratorAgent
from app.agents.generate_summary_agent import GenerateSummaryAgent
from app.core.vector_storage import init_chroma_db
from app.core.embedding_generator import get_embeddings_model
from app.core.pdf_loader import load_pdf

def init_agent():
    collection = init_chroma_db()
    embeddings = get_embeddings_model()
    agent = OrchestratorAgent(collection=collection)
    return agent

# Streamlit UI layout
def main():
    st.title("PDF Query Answering System")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if uploaded_file is not None:
        # Saving the uploaded file to a temporary location
        with open("temp_uploaded_file.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded successfully!")
        
        # Initialize agents
        agent = init_agent()
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
                    response = agent.answer_query(query=query, filepath="temp_uploaded_file.pdf")
                    
                    # Displaying the response
                    st.subheader("Answer:")
                    st.write(response)
                    
                    # Store Q&A in session state
                    if 'qa_history' not in st.session_state:
                        st.session_state.qa_history = []
                    st.session_state.qa_history.append({
                        'question': query,
                        'answer': response
                    })
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
                    st.info("Please try rephrasing your question.")
        
        # Display Q&A history
        if 'qa_history' in st.session_state and st.session_state.qa_history:
            st.subheader("Q&A History")
            for qa in st.session_state.qa_history:
                st.write(f"Q: {qa['question']}")
                st.write(f"A: {qa['answer']}")
                st.write("---")


if __name__ == "__main__":
    main()
