import pymupdf

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = pymupdf.open(pdf_path)
    complete_text = ''
    
    try:
        for page in doc: # iterate the document pages
            text = page.get_text() # get text of page
            complete_text += text # write text of page
        return complete_text.strip()
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""