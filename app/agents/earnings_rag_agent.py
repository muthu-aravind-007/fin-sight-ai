from app.rag.pdf_loader import load_pdf
from app.rag.chunker import chunk_documents

from app.rag.vector_store import create_vector_store
from app.rag.load_vector_store import load_vector_store
from app.rag.retriever import get_retriever

from app.prompts.rag_prompt import build_rag_prompt
from app.services.llm_service import generate_analysis


def index_earnings_pdf(
    pdf_path,
    persist_directory,
):
    """
    Load a PDF, split it into chunks,
    create embeddings, and persist
    the Chroma vector database.
    """

    docs = load_pdf(pdf_path)

    chunks = chunk_documents(docs)

    create_vector_store(
        documents=chunks,
        persist_directory=persist_directory,
    )

    return {
        "message": "PDF indexed successfully.",
        "persist_directory": persist_directory,
        "chunks": len(chunks),
    }


def query_earnings_pdf(
    question,
    persist_directory,
):
    """
    Query an existing Chroma vector store.
    """

    db = load_vector_store(
        persist_directory
    )

    retriever = get_retriever(
        db
    )

    results = retriever.invoke(
        question
    )

    context = "\n\n".join(
        doc.page_content
        for doc in results
    )

    source_pages = sorted(
        {
            doc.metadata.get("page", 0) + 1
            for doc in results
        }
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
        "source_pages": source_pages,
    }