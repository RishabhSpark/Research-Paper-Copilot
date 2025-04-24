from app.core.pdf_loader import load_pdf

if __name__ == "__main__":
    path = "public/sample_papers/A_brief_history_of_Pfizer_Central_Research.pdf"
    documents = load_pdf(path)

    page_num = 2
    print(f"\n--- Preview Page {page_num+1} Content ---")
    print(documents[page_num].page_content)