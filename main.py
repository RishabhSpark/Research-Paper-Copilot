import os
from app.agents.orchestrator import OrchestratorAgent
from app.core.vector_storage import init_chroma_db
from dotenv import load_dotenv

load_dotenv()

def main():
    chroma_collection = init_chroma_db()

    # Initialize Orchestrator
    orchestrator = OrchestratorAgent(collection=chroma_collection)

    # Prompt user for the PDF file and the query
    filepath = input("Please enter the path to the PDF file: ").strip()
    # filepath = 'C:/Users/khand/OneDrive/Desktop/Rishabh/Agentic AI/Research Paper Copilot/Research-Paper-Copilot/public/sample_papers/A_brief_history_of_Pfizer_Central_Research.pdf'
    query = input("Please enter your query: ").strip()
    # query = "Can you list the Pfizer products that failed to reach the market?"

    # Check if file exists
    if not os.path.isfile(filepath):
        print(f"[ERROR] The file '{filepath}' does not exist. Please check the path and try again.")
        return

    # Call Orchestrator to answer the query
    try:
        response = orchestrator.answer_query(query=query, filepath=filepath, top_k=5)
        print("\nResponse:")
        print(response)
    except Exception as e:
        print(f"[ERROR] An error occurred while processing the query: {str(e)}")

if __name__ == "__main__":
    main()