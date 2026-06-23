from langchain_community.retrievers import BM25Retriever


def get_bm25_retriever(
    chunks
):

    retriever = BM25Retriever.from_documents(
        chunks
    )

    retriever.k = 12

    return retriever