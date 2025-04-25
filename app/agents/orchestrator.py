from .pdf_loader_agent import PDFLoaderAgent
from .embeddings_generation_agent import EmbeddingGenerationAgent
from .chroma_storage_agent import ChromaStorageAgent
from .document_retrieval_agent import DocumentRetrievalAgent
from .text_chunking_agent import TextChunkingAgent
from .prompt_builder_agent import PromptBuilderAgent
from .response_generation_agent import ResponseGenerationAgent
from .clarification_agent import ClarificationAgent
from chromadb.api.models import Collection

class OrchestratorAgent:
    def __init__(self, collection: Collection):
        self.pdf_loader_agent = PDFLoaderAgent()
        self.embeddings_generation_agent = EmbeddingGenerationAgent()
        self.chromadb_storage_agent = ChromaStorageAgent(collection=collection)
        self.retrieval_agent = DocumentRetrievalAgent(collection= collection)
        self.chunking_agent = TextChunkingAgent()
        self.prompt_builder_agent = PromptBuilderAgent()
        self.response_agent = ResponseGenerationAgent()
        self.clarification_agent = ClarificationAgent()

    def answer_query(self, query: str, filepath: str, top_k: int = 5) -> str:
        """Orchestrates the agents to answer the query."""
         # Step 1: Load PDF
        documents = self.pdf_loader_agent.load_pdf(filepath)
        if not documents:
            return "No content found in the PDF. Please check the file."
        print("Documents loaded")

        # Step 2: Chunk the documents
        chunked_docs = self.chunking_agent.chunk_documents(documents)
        print("Docs chunked")

        # Step 3: Generate embeddings for chunked documents
        embeddings = self.embeddings_generation_agent.generate_embeddings(chunked_docs)
        print("Embeddings generated")
        # print(embeddings)

        # Step 4: Store embeddings in ChromaDB
        self.chromadb_storage_agent.store_embeddings(chunked_docs, embeddings)
        print("Embeddings stored in ChromaDB")

        # Step 5: Retrieve documents based on query
        docs, metas = self.retrieval_agent.retrieve_documents(query=query)
    
        if not docs:
            return self.clarification_agent.ask_for_clarification(query=query)
        print("Retrieved docs based on query")

        # Step 6: Format the documents into a context string
        context = [doc.page_content for doc in docs]
        print("Formatted the documents into a context string")
        # print(context)

        # Step 7: Build prompt and generate response
        prompt = self.prompt_builder_agent.build_prompt(query=query, docs=context)
        response = self.response_agent.generate_response(prompt=prompt)
        print("Response generated")

        return response