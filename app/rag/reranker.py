from sentence_transformers import CrossEncoder

_reranker = None


def get_reranker():

    global _reranker

    if _reranker is None:

        _reranker = CrossEncoder(
            "BAAI/bge-reranker-base"
        )

    return _reranker


def rerank_documents(
    question,
    documents,
    top_k=10
):

    reranker = get_reranker()

    pairs = [
        (question, doc.page_content)
        for doc in documents
    ]

    scores = reranker.predict(
        pairs
    )

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        doc
        for doc, _
        in ranked[:top_k]
    ]