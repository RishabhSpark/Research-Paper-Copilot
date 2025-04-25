from app.retriever.document_retriever import retrieve_relevant_documents
from app.core.prompt_builder import format_documents, build_prompt
from app.core.gemini_client import generate_response
from chromadb.api.models.Collection import Collection

def answer_query_with_context(query: str, collection: Collection, top_k: int = 5) -> str:
    """Full RAG pipeline: retrieve, build prompt, and get response from Gemini."""
    docs, metas = retrieve_relevant_documents(query, collection, top_k=top_k)
    context = format_documents(docs)
    prompt = build_prompt(query, context)
    response = generate_response(prompt)

    return response, metas