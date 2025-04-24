# from sentence_transformers import SentenceTransformer
# from langchain.schema import Document
# from typing import List

# model = SentenceTransformer('all-MiniLM-L6-v2')

# def embed_documents(documents: List[Document]) -> List[List[float]]:
#     """Generate embeddings for each chunked document using Sentence-Transformers.

#     Args:
#         documents (List[Document]): List of chunked documents.  

#     Returns:
#         List[List[float]]: A list of embeddings (vectors) for each document chunk.
#     """
#     embeddings = []
    
#     for doc in documents:
#         embedding = model.encode(doc.page_content)
#         embeddings.append(embedding)

#     print(f'Generated embeddings for {len(documents)} chunks.')

#     return embeddings

# src/core/embedding_generator.py

from langchain.embeddings import HuggingFaceEmbeddings

def get_embeddings_model(model_name="all-MiniLM-L6-v2"):
    """Return an embeddings model from HuggingFace."""
    return HuggingFaceEmbeddings(model_name=model_name)

def generate_embeddings(documents, embeddings_model):
    """Generate embeddings for a list of documents."""
    texts = [doc.page_content for doc in documents]
    return embeddings_model.embed_documents(texts)