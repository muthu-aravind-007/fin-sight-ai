from app.rag.pdf_loader import load_pdf
from app.rag.chunker import chunk_documents
from app.rag.vector_store import create_vector_store
from app.rag.retriever import get_retriever

docs = load_pdf(
    "data/transcripts/nvda_q1_2027.pdf"
)

chunks = chunk_documents(
    docs
)

db = create_vector_store(
    chunks
)

retriever = get_retriever(
    db
)

results = retriever.invoke(
    "What did management say about AI demand?"
)

for doc in results:
    print("\n")
    print(doc.page_content[:500])