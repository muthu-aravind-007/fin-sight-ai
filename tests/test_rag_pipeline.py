# tests/test_rag_pipeline.py

from app.rag.pdf_loader import load_pdf
from app.rag.chunker import chunk_documents

docs = load_pdf(
    "data/transcripts/nvda_q1_2027.pdf"
)

chunks = chunk_documents(
    docs
)

print("Pages:", len(docs))
print("Chunks:", len(chunks))

print("\nFirst Chunk:\n")
print(
    chunks[0].page_content[:1000]
)