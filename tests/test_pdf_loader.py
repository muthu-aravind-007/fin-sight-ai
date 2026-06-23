# tests/test_pdf_loader.py

from app.rag.pdf_loader import load_pdf

docs = load_pdf(
    "data/transcripts/nvda_q1_2027.pdf"
)

print("Pages:", len(docs))
print(docs[0].page_content[:300])