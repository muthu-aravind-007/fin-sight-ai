
import os
import time
from sentence_transformers import CrossEncoder

# Reranking is enabled by default.
RERANKER_MODEL = os.getenv(
    "RERANKER_MODEL",
    "BAAI/bge-reranker-base",
)

_reranker = None


def get_reranker():
    global _reranker

    if _reranker is None:
        print(f"Loading cross-encoder reranker: {RERANKER_MODEL}")
        _reranker = CrossEncoder(RERANKER_MODEL)

    return _reranker


def rerank_documents(question, documents, top_k=10):
    if not documents:
        return []

    # Enabled by default; can still be explicitly disabled if needed.
    enabled = os.getenv("ENABLE_RERANKER", "true").strip().lower() in {
        "1", "true", "yes", "on"
    }

    if not enabled:
        print(
            f"Reranker disabled; keeping first "
            f"{min(top_k, len(documents))} of {len(documents)} documents."
        )
        return documents[:top_k]

    reranker = get_reranker()

    pairs = [
        (question, doc.page_content)
        for doc in documents
    ]

    start = time.perf_counter()
    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda item: float(item[1]),
        reverse=True,
    )

    selected = [
        doc for doc, _ in ranked[:top_k]
    ]

    print(
        f"Cross-encoder reranked {len(documents)} chunks "
        f"in {time.perf_counter() - start:.2f} sec."
    )

    return selected
