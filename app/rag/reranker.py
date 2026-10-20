
import os
from sentence_transformers import CrossEncoder

_reranker = None


def get_reranker():
    global _reranker

    if _reranker is None:
        model_name = os.getenv(
            "RERANKER_MODEL",
            "BAAI/bge-reranker-base"
        )

        _reranker = CrossEncoder(model_name)

    return _reranker


def rerank_documents(question, documents, top_k=10):
    if not documents:
        return []

    # Optional fallback: skip reranking if disabled.
    if os.getenv("ENABLE_RERANKER", "true").lower() != "true":
        return documents[:top_k]

    reranker = get_reranker()

    pairs = [
        (question, doc.page_content)
        for doc in documents
    ]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        doc for doc, _ in ranked[:top_k]
    ]
