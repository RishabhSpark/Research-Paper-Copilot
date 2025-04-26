import chromadb
from langchain.schema import Document
from chromadb.api.models import Collection
from typing import List, Callable

def init_chroma_db() -> Collection:
    """Initializes chroma client and creates a function"""
    client = chromadb.Client()

    try:
        collection = client.get_collection("document_embeddings")
    except Exception as e:
        collection = client.create_collection(name="document_embeddings")

    return collection

def add_embeddings_to_chroma(
        documents: List[Document], 
        embeddings, 
        collection: Collection) -> None:
    """Add embeddings and documents to Chroma collection."""
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]

    embeddings_data = embeddings

    # Generate unique ids for each document
    ids = [f"doc_{i}" for i in range(len(documents))]

    collection.add(
        ids = ids,
        documents = texts,
        metadatas = metadatas,
        embeddings = embeddings_data
    )

    print(f"[CHROMA] Added {len(documents)} documents to Chroma database.")


def query_chroma(
        query: str, 
        collection: Collection, 
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