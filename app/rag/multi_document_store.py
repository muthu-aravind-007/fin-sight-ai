
import hashlib
import json
import os
CACHE_VERSION = "v2_ocr"

from app.rag.vector_store import create_vector_store
from app.rag.load_vector_store import load_vector_store

def build_cache_key(documents):
    """
    Generate a stable cache key from document metadata
    and file contents.
    """
    entries = []

    for doc in documents:
        pdf_path = doc["pdf_path"]

        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        digest = hashlib.sha256()

        with open(pdf_path, "rb") as file:
            for block in iter(
                lambda: file.read(1024 * 1024),
                b"",
            ):
                digest.update(block)

        entries.append({
            "cache_version": CACHE_VERSION,
            "company": doc["company"].strip().upper(),
            "quarter": doc["quarter"].strip().upper(),
            "sha256": digest.hexdigest(),
        })

    entries.sort(
        key=lambda item: (
            item["company"],
            item["quarter"],
            item["sha256"],
        )
    )

    serialized = json.dumps(
        entries,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()



def build_multi_document_store(
    all_chunks,
    cache_key,
):
    persist_directory = os.path.join(
        "chroma_db",
        cache_key,
    )

    if os.path.isdir(persist_directory):
        print("Loading cached vector store...")

        return load_vector_store(
            persist_directory
        )

    if not all_chunks:
        raise ValueError(
            "Cannot create a vector store without document chunks."
        )

    print("Creating new vector store...")

    return create_vector_store(
        all_chunks,
        persist_directory,
    )
