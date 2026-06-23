from app.rag.pdf_loader import load_pdf
from app.rag.chunker import chunk_documents

from app.prompts.transcript_summary_prompt import (
    build_transcript_summary_prompt
)

from app.services.llm_service import (
    generate_analysis
)


def summarize_transcript(
    pdf_path
):

    docs = load_pdf(
        pdf_path
    )

    chunks = chunk_documents(
        docs
    )

    context = "\n\n".join(
        [
            chunk.page_content
            for chunk in chunks[:15]
        ]
    )

    prompt = build_transcript_summary_prompt(
        context
    )

    summary = generate_analysis(
        prompt
    )

    return {
        "summary": summary
    }