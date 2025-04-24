import sys
import os
import pytest
from reportlab.pdfgen import canvas

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app')))
from core.pdf_loader import load_pdf

# def test_pdf_loading_valid():
#     docs = load_pdf("public/sample_papers/A_brief_history_of_Pfizer_Central_Research.pdf")
#     assert len(docs) > 0

# def test_pdf_loading_invalid_filetype():
#     with pytest.raises(ValueError):
#         load_pdf("public/sample_papers/A_brief_history_of_Pfizer_Central_Research.txt")

# def test_pdf_loading_file_not_found():
#     with pytest.raises(FileNotFoundError):
#         load_pdf("public/sample_papers/invalid_file.pdf")

def test_pdf_loading_valid(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    # Generate a valid PDF using reportlab
    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 750, "This is a test PDF.")
    c.save()

    docs = load_pdf(str(pdf_path))
    assert len(docs) > 0

def test_pdf_loading_invalid_filetype(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Not a PDF")

    with pytest.raises(ValueError):
        load_pdf(str(test_file))

def test_pdf_loading_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_pdf("public/sample_papers/invalid_file.pdf")