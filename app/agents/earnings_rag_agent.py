from app.rag.pdf_loader import load_pdf
from app.rag.chunker import chunk_documents
from app.rag.vector_store import create_vector_store
from app.rag.retriever import get_retriever

from app.prompts.rag_prompt import build_rag_prompt

from app.services.llm_service import generate_analysis


def analyze_earnings_rag(
    pdf_path,
    question
):

    docs = load_pdf(
        pdf_path
    )

    chunks = chunk_documents(
        docs
    )

    db = create_vector_store(
        chunks
    )

    retriever = get_retriever(
        db
    )

    results = retriever.invoke(
        question
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in results
        ]
    )

    source_pages = []

    for doc in results:

        page = doc.metadata.get(
            "page",
            0
        )

        source_pages.append(
            page + 1
        )

    prompt = build_rag_prompt(
        context,
        question
    )

    answer = generate_analysis(
        prompt
    )

    return {
        "question": question,
        "answer": answer,
        "context": context,
        "source_pages": list(
            set(source_pages)
        )
    }