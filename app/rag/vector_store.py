from langchain_chroma import Chroma
from app.rag.embeddings import get_embedding_model


def create_vector_store(
    documents,
    persist_directory,
    collection_name="earnings"
):

    return Chroma.from_documents(
        documents=documents,
        embedding=get_embedding_model(),
        persist_directory=persist_directory,
        collection_name=collection_name,
    )