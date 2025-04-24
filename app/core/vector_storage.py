import chromadb
from langchain.schema import Document
from typing import List, Callable

def init_chroma_db() -> chromadb.api.models.Collection.Collection:
    """Initializes chroma client and creates a function"""
    client = chromadb.Client()
    collection = client.create_collection(name="document_embeddings")
    return collection

def add_embeddings_to_chroma(
        documents: List[Document], 
        embeddings: Callable[[List[str]], 
        List[List[float]]], 
        collection: chromadb.api.models.Collection.Collection) -> None:
    """Add embeddings and documents to Chroma collection."""
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]

    embeddings_data = embeddings.embed_documents(texts)

    collection.add(
        documents = texts,
        metadatas = metadatas,
        embeddings = embeddings_data
    )

    print(f"[CHROMA] Added {len(documents)} documents to Chroma database.")


def query_chroma(
        query: str, 
        collection: chromadb.api.models.Collection.Collection, 
        embed_query_fn: Callable[[str], List[float]], 
        top_k:int = 5):
    """Query Chroma database for similar documents."""
    query_embedding = embed_query_fn.embed_query(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    docs = results.get("documents", [[]])[0]  # Unwrap the nested list
    metas = results.get("metadatas", [[]])[0]  # Unwrap metadata


    print(f"[CHROMA] Found {len(docs)} similar documents.")
    print(f"[CHROMA] Document IDs: {docs}")
    print(f"[CHROMA] Metadatas: {metas}")

    return docs, metas