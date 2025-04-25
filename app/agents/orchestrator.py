from agents.document_retrieval_agent import DocumentRetrievalAgent
from agents.text_chunking_agent import TextChunkingAgent
from agents.prompt_builder_agent import PromptBuilderAgent
from agents.response_generation_agent import ResponseGenerationAgent
from agents.clarification_agent import ClarificationAgent
from chromadb.api.models import Collection
from typing import List

class OrchestratorAgent:
    def __init__(self, collection: Collection):
        self.retrieval_agent = DocumentRetrievalAgent(collection=collection)
        self.chunking_agent = TextChunkingAgent()
        self.prompt_builder_agent = PromptBuilderAgent()
        self.response_agent = ResponseGenerationAgent()
        self.clarification_agent = ClarificationAgent()

    def answer_query(self, query: str, top_k: int = 5) -> str:
        """Orchestrates the agents to answer the query."""
        docs, metas = self.retrieval_agent.retrieve_documents(query=query)

        if not docs:
            return self.clarification_agent.ask_for_clarification(query=query)
        
        chunked_docs = self.chunking_agent.chunk_documents(docs)

        # Format the documents into a context string
        context = [doc.page_content for doc in chunked_docs]

        prompt = self.prompt_builder_agent.build_prompt(query=query, docs=context)

        response = self.response_agent.generate_response(prompt=prompt)

        return response