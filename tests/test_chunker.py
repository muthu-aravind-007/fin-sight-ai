# tests/test_chunker.py

from app.rag.chunker import chunk_documents
from langchain_core.documents import Document

docs = [
    Document(
        page_content="NVIDIA revenue increased significantly. " * 100
    )
]

chunks = chunk_documents(docs)

print("Chunks:", len(chunks))
print(chunks[0].page_content[:100])