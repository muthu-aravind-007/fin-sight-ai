
import hashlib
import os
import pickle

from app.rag.pdf_loader import load_pdf
from app.rag.chunker import chunk_documents


CACHE_VERSION = "v1"
CACHE_DIRECTORY = os.path.join(
    "cache",
    "processed_chunks",
)


def _get_cache_key(pdf_path, company, quarter):
    digest = hashlib.sha256()

    with open(pdf_path, "rb") as file:
        for block in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    cache_data = "|".join([
        CACHE_VERSION,
        company.strip().upper(),
        quarter.strip().upper(),
        digest.hexdigest(),
    ])

    return hashlib.sha256(
        cache_data.encode("utf-8")
    ).hexdigest()


def process_document(pdf_path, company, quarter):
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    os.makedirs(CACHE_DIRECTORY, exist_ok=True)

    cache_key = _get_cache_key(
        pdf_path,
        company,
        quarter,
    )

    cache_path = os.path.join(
        CACHE_DIRECTORY,
        f"{cache_key}.pkl",
    )

    # Reuse previously extracted and cleaned chunks.
    if os.path.isfile(cache_path):
        try:
            with open(cache_path, "rb") as file:
                chunks = pickle.load(file)

            print(
                f"Loaded processed chunks from cache: "
                f"{company} {quarter}"
            )

            return chunks

        except (
            OSError,
            pickle.UnpicklingError,
            EOFError,
            AttributeError,
            ImportError,
            ValueError,
        ):
            print(
                f"Invalid document cache; reprocessing: "
                f"{company} {quarter}"
            )

    print(
        f"Processing PDF: {company} {quarter}"
    )

    docs = load_pdf(pdf_path)
    chunks = chunk_documents(docs)

    cleaned_chunks = []

    for chunk in chunks:
        text = chunk.page_content.lower()

        footer_hits = sum([
            "factset callstreet" in text,
            "copyright" in text,
            "1-877-factset" in text,
        ])

        if footer_hits >= 3:
            continue

        if len(text.strip()) < 150:
            continue

        chunk.metadata["company"] = (
            company.strip().upper()
        )
        chunk.metadata["quarter"] = (
            quarter.strip().upper()
        )
        chunk.metadata["source"] = pdf_path

        cleaned_chunks.append(chunk)

    # Save the cleaned chunks for subsequent questions.
    temporary_path = cache_path + ".tmp"

    with open(temporary_path, "wb") as file:
        pickle.dump(
            cleaned_chunks,
            file,
            protocol=pickle.HIGHEST_PROTOCOL,
        )

    os.replace(temporary_path, cache_path)

    print(
        f"Cached {len(cleaned_chunks)} chunks: "
        f"{company} {quarter}"
    )

    return cleaned_chunks
