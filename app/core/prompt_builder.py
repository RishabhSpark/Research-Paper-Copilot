from typing import List

def format_documents(docs: List[str]) -> str:
    """Convert list of documents into readable strings."""
    return "\n\n".join([f'Document {i+1}:\n{doc}' for i, doc in enumerate(docs)])

def build_prompt(query: str, context: str) -> str:
    """Construct prompt to send to gemini"""
    prompt =  f"""
    You are an intelligent assistant. Use the context below to answer the questions.

    Context:
    {context}

    Question:
    {query}

    Answer:"""

    return prompt