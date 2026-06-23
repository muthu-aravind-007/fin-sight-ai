from langchain_chroma import Chroma

from app.rag.embeddings import (
    embedding_model
)


def create_vector_store(
    documents,
    persist_directory
):

    db = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    return db