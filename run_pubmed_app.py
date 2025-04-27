import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from app.main_pubmed_app import main

if __name__ == "__main__":
    main() 