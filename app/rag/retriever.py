from app.rag.vector_store import (
    create_vector_store
)


def retrieve_documents(
    documents,
    query
):

    db = create_vector_store(
        documents
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever.invoke(
        query
    )