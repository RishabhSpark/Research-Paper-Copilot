# from app.agents.orchestrator import OrchestratorAgent
# from app.core.vector_storage import init_chroma_db, add_embeddings_to_chroma
# from app.core.embedding_generator import get_embeddings_model, generate_embeddings
# from app.core.pdf_loader import load_pdf
# from app.agents.orchestrator import OrchestratorAgent

# # Step 1: Load documents
# documents = load_pdf("public/sample_papers/A_brief_history_of_Pfizer_Central_Research.pdf")

# # Step 2: Get embeddings model and encode
# embed_model = get_embeddings_model()
# embeddings = generate_embeddings(documents = documents, embeddings_model=embed_model)

# # Step 3: Initialize DB + collection
# collection = init_chroma_db()

# # Step 4: Add embeddings to Chroma
# add_embeddings_to_chroma(documents=documents, embeddings=embed_model, collection=collection)

# # Step 5: Run orchestrator
# orchestrator = OrchestratorAgent(collection=collection)
# query = "Can you list the Pfizer products that failed to reach the market?"
# response = orchestrator.answer_query(query=query, top_k=10)

# print("Answer:\n", response)

import os
from app.agents.orchestrator import OrchestratorAgent
from app.core.vector_storage import init_chroma_db  # Import your init_chroma_db function
from dotenv import load_dotenv

# Load environment variables (if you have any sensitive information like API keys or paths in .env file)
load_dotenv()

def main():
    chroma_collection = init_chroma_db()

    # Initialize Orchestrator
    orchestrator = OrchestratorAgent(collection=chroma_collection)

    # Prompt user for the PDF file and the query
    # filepath = input("Please enter the path to the PDF file: ").strip()
    filepath = 'C:/Users/khand/OneDrive/Desktop/Rishabh/Agentic AI/Research Paper Copilot/Research-Paper-Copilot/public/sample_papers/A_brief_history_of_Pfizer_Central_Research.pdf'
    # query = input("Please enter your query: ").strip()
    query = "Can you list the Pfizer products that failed to reach the market?"

    # Check if file exists
    if not os.path.isfile(filepath):
        print(f"[ERROR] The file '{filepath}' does not exist. Please check the path and try again.")
        return

    # Call Orchestrator to answer the query
    try:
        response = orchestrator.answer_query(query=query, filepath=filepath)
        print("\nResponse:")
        print(response)
    except Exception as e:
        print(f"[ERROR] An error occurred while processing the query: {str(e)}")

if __name__ == "__main__":
    main()