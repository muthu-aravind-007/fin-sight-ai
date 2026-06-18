# tests/test_embeddings.py

from app.rag.embeddings import (
    embedding_model
)

vector = embedding_model.embed_query(
    "NVIDIA revenue growth"
)

print(len(vector))