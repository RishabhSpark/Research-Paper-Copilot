import sys
import os
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*builtin type.*")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app')))
from data.pdf_utils import extract_text_from_pdf

def test_extract_text_from_pdf_returns_non_empty_string():
    pdf_path = "public/sample_papers/A_brief_history_of_Pfizer_Central_Research.pdf"
    
    assert os.path.exists(pdf_path), "PDF file does not exist!"
    
    extracted_text = extract_text_from_pdf(pdf_path)
    
    assert isinstance(extracted_text, str), "Output should be a string"
    assert len(extracted_text) > 10, "Extracted text seems too short — check the PDF or logic"