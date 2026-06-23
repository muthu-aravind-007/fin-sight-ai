import os

from app.rag.vector_store import (
    create_vector_store
)

from app.rag.load_vector_store import (
    load_vector_store
)


def build_multi_document_store(
    all_chunks,
    cache_key
):

    persist_directory = (
        f"chroma_db/{cache_key}"
    )

    if os.path.exists(
        persist_directory
    ):

        print(
            "Loading cached vector store..."
        )

        return load_vector_store(
            persist_directory
        )

    print(
        "Creating new vector store..."
    )

    return create_vector_store(
        all_chunks,
        persist_directory
    )