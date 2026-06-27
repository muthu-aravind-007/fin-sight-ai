from langchain_chroma import Chroma
from app.rag.embeddings import get_embedding_model

def load_vector_store(
    persist_directory,
    collection_name="earnings",
):

    return Chroma(
        persist_directory=persist_directory,
        embedding_function=get_embedding_model(),
        collection_name=collection_name,
    )