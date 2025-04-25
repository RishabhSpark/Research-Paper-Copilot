from app.core.gemini_client import generate_response
from typing import List

class ResponseGenerationAgent:
    def generate_response(self, prompt: str) -> str:
        """Generate a response from Gemini."""
        return generate_response(prompt)