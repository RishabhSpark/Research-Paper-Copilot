class ClarificationAgent:
    def ask_for_clarification(self, query: str) -> str:
        """Ask for clarification if the query is unclear."""
        return f"Sorry. The query '{query}' is ambiguous. Could you please clarify your question?"