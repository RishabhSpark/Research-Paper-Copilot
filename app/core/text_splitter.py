from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List

def chunk_documents(documents: List[Document], chunk_size: int=500, chunk_overlap: int=100) -> List[Document]:
    """Split each document into smaller overlapping chunks.

    Args:
        documents List of LangChain Document objects (from PDF).
        chunk_size (int, optional): Number of characters per chunk. Defaults to 500.
        chunk_overlap (int, optional): Overlap between chunks for context continuity. Defaults to 500.

    Returns:
        List[Document]: List of chunked Document objects.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunked_docs = splitter.split_documents(documents)
    print(f'[CHUNKER] split documents into {len(chunked_docs)} chunks.')

    return chunked_docs