from langchain_community.vectorstores import Chroma

from app.rag.embeddings import (
    embedding_model
)


def load_vector_store(
    persist_directory
):

    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )