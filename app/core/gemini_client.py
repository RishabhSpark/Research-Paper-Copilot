import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(prompt: str) -> str:
    """Sends a prompt to gemini to get a response."""
    print('[GEMINI] Sending prompt...')
    response = model.generate_content(prompt)
    return response.text