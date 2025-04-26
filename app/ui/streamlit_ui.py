import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.agents.orchestrator import OrchestratorAgent
from app.core.vector_storage import init_chroma_db
from app.core.embedding_generator import get_embeddings_model

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

        # Text input for query
        query = st.text_input("Ask your question:")

        if query:
            agent = init_agent()
            
            # Using the uploaded PDF to process the query
            response = agent.answer_query(query=query, filepath="temp_uploaded_file.pdf")
            
            # Displaying the response
            st.write("Answer:")
            st.write(response)


if __name__ == "__main__":
    main()
