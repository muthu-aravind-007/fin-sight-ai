from app.rag.pdf_loader import load_pdf
from app.rag.chunker import chunk_documents


def process_document(
    pdf_path,
    company,
    quarter
):

    docs = load_pdf(pdf_path)

    chunks = chunk_documents(docs)

    cleaned_chunks = []

    for chunk in chunks:

        text = chunk.page_content.lower()

        footer_hits = 0

        if "factset callstreet" in text:
            footer_hits += 1

        if "copyright" in text:
            footer_hits += 1

        if "1-877-factset" in text:
            footer_hits += 1

        if footer_hits >= 3:
            continue

        if len(text.strip()) < 150:
            continue

        chunk.metadata["company"] = company
        chunk.metadata["quarter"] = quarter
        chunk.metadata["source"] = pdf_path

        cleaned_chunks.append(chunk)

    return cleaned_chunks