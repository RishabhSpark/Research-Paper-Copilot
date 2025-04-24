from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from typing import List

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_documents(documents: List[Document]) -> List[List[float]]:
    """Generate embeddings for each chunked document using Sentence-Transformers.

    Args:
        documents (List[Document]): List of chunked documents.  

    Returns:
        List[List[float]]: A list of embeddings (vectors) for each document chunk.
    """
    embeddings = []
    
    for doc in documents:
        embedding = model.encode(doc.page_content)
        embeddings.append(embedding)

    print(f'Generated embeddings for {len(documents)} chunks.')

    return embeddings