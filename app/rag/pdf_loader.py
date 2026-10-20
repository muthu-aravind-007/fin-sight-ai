import hashlib
import os
import pickle

from langchain_community.document_loaders import PyPDFLoader


EXTRACTION_CACHE_VERSION = "v1"
CACHE_DIRECTORY = os.path.join(
    "cache",
    "extracted_pdfs",
)


def _file_hash(path):
    digest = hashlib.sha256()

    with open(path, "rb") as file:
        for block in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def _extract_pdf(path):
    # First, try normal text extraction.
    loader = PyPDFLoader(path)
    documents = loader.load()

    extracted_text = "\n".join(
        doc.page_content.strip()
        for doc in documents
        if doc.page_content and doc.page_content.strip()
    )

    # Return normally extracted text when available.
    if len(extracted_text) >= 100:
        return documents

    print(
        f"Little or no selectable text found in {path}. "
        "Trying OCR..."
    )

    try:
        import pytesseract
        from pdf2image import convert_from_path
        from langchain_core.documents import Document

        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        poppler_path = (
            r"C:\Users\HP\Downloads\Release-26.09.0-0"
            r"\poppler-26.09.0\Library\bin"
        )

        images = convert_from_path(
            path,
            dpi=200,
            poppler_path=poppler_path,
        )

        ocr_documents = []

        for page_number, image in enumerate(images):
            text = pytesseract.image_to_string(
                image,
                lang="eng",
            ).strip()

            if text:
                ocr_documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": path,
                            "page": page_number,
                        },
                    )
                )

        if not ocr_documents:
            raise ValueError(
                f"OCR did not extract text from {path}"
            )

        print(
            f"OCR extracted text from "
            f"{len(ocr_documents)} pages."
        )

        return ocr_documents

    except Exception as exc:
        raise RuntimeError(
            f"PDF text extraction and OCR both failed "
            f"for {path}: {exc}"
        ) from exc


def load_pdf(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"PDF not found: {path}"
        )

    os.makedirs(CACHE_DIRECTORY, exist_ok=True)

    cache_key = hashlib.sha256(
        (
            EXTRACTION_CACHE_VERSION
            + ":"
            + _file_hash(path)
        ).encode("utf-8")
    ).hexdigest()

    cache_path = os.path.join(
        CACHE_DIRECTORY,
        f"{cache_key}.pkl",
    )

    if os.path.isfile(cache_path):
        try:
            with open(cache_path, "rb") as file:
                documents = pickle.load(file)

            if (
                isinstance(documents, list)
                and all(
                    hasattr(doc, "page_content")
                    and hasattr(doc, "metadata")
                    for doc in documents
                )
            ):
                print(
                    f"Loaded extracted PDF from cache: "
                    f"{os.path.basename(path)}"
                )
                return documents

        except (
            OSError,
            pickle.UnpicklingError,
            EOFError,
            AttributeError,
            ImportError,
            ValueError,
        ):
            print(
                f"Invalid extraction cache; re-extracting: "
                f"{os.path.basename(path)}"
            )

    documents = _extract_pdf(path)

    temporary_path = cache_path + ".tmp"

    with open(temporary_path, "wb") as file:
        pickle.dump(
            documents,
            file,
            protocol=pickle.HIGHEST_PROTOCOL,
        )

    os.replace(temporary_path, cache_path)

    print(
        f"Cached extracted PDF: "
        f"{os.path.basename(path)}"
    )

    return documents
