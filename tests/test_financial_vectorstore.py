# tests/test_financial_vectorstore.py

from app.rag.pdf_loader import load_pdf
from app.rag.chunker import chunk_documents
from app.rag.vector_store import create_vector_store

docs = load_pdf(
    "data/transcripts/nvda_q1_2027.pdf"
)

chunks = chunk_documents(
    docs
)

db = create_vector_store(
    chunks
)

print(
    db._collection.count()
)