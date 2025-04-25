from app.core.prompt_builder import format_documents, build_prompt
from typing import List


class PromptBuilderAgent:
    def __init__(self, top_k: int = 5):
        self.top_k = top_k

    def build_prompt(self, query: str, docs: List[str]) -> str:
        """Construct the prompt for the next agent (Gemini response generator)."""
        context = format_documents(docs)
        return build_prompt(query, context)

    def run(self, query: str, docs: List[str]) -> str:
        """Run the full agent workflow (format documents, build prompt)."""
        return self.build_prompt(query, docs)