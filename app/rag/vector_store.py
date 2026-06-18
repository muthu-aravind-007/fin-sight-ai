from langchain_community.vectorstores import Chroma

from app.rag.embeddings import (
    embedding_model
)


def create_vector_store(
    documents
):

    return Chroma.from_documents(
        documents,
        embedding_model,
        persist_directory="chroma_db"
    )