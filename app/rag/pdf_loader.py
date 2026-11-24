
import hashlib
import os
import pickle
import shutil
import sys
import gc

from langchain_community.document_loaders import PyPDFLoader
from pdf2image import convert_from_path, pdfinfo_from_path


EXTRACTION_CACHE_VERSION = "v1"
CACHE_DIRECTORY = os.path.join(
    "cache",
    "extracted_pdfs",
)


def _log_memory(stage):
    """Log current and peak process memory on Linux."""
    try:
        memory_values = {}

        with open("/proc/self/status", "r") as file:
            for line in file:
                if line.startswith(("VmRSS:", "VmHWM:")):
                    key, value = line.split(":", 1)
                    memory_values[key] = int(
                        value.strip().split()[0]
                    )

        current_mb = memory_values.get("VmRSS")
        peak_mb = memory_values.get("VmHWM")

        if current_mb is not None:
            print(
                f"[MEMORY] {stage} | "
                f"Current: {current_mb / 1024:.1f} MB | "
                f"Peak: {peak_mb / 1024:.1f} MB"
                if peak_mb is not None
                else
                f"[MEMORY] {stage} | "
                f"Current: {current_mb / 1024:.1f} MB"
            )
        else:
            print(
                f"[MEMORY] {stage} | "
                "Memory information unavailable."
            )

    except (OSError, ValueError) as exc:
        print(
            f"[MEMORY] {stage} | "
            f"Could not read memory information: {exc}"
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
    _log_memory("Before normal PDF extraction")

    # First, try normal text extraction.
    loader = PyPDFLoader(path)
    documents = loader.load()

    _log_memory("After normal PDF extraction")

    extracted_text = "\n".join(
        doc.page_content.strip()
        for doc in documents
        if doc.page_content and doc.page_content.strip()
    )

    # Return normally extracted text when available.
    if len(extracted_text) >= 100:
        print(
            f"Normal text extraction successful for {path}."
        )
        return documents

    print(
        f"Little or no selectable text found in {path}. "
        "Trying OCR..."
    )

    _log_memory("Before OCR initialization")

    try:
        import pytesseract
        from langchain_core.documents import Document

        if sys.platform == "win32":
            pytesseract.pytesseract.tesseract_cmd = (
                r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )

            poppler_path = (
                r"C:\Users\HP\Downloads\Release-26.09.0-0"
                r"\poppler-26.09.0\Library\bin"
            )

        else:
            tesseract_path = shutil.which("tesseract")
            pdfinfo_path = shutil.which("pdfinfo")

            if not tesseract_path or not pdfinfo_path:
                raise RuntimeError(
                    "Tesseract or Poppler is not installed "
                    "or not available in PATH."
                )

            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            poppler_path = os.path.dirname(pdfinfo_path)

        total_pages = pdfinfo_from_path(
            path,
            poppler_path=poppler_path,
        )["Pages"]

        print(f"Starting OCR for {total_pages} pages.")

        ocr_documents = []

        _log_memory("Before OCR page processing")

        for page_number in range(total_pages):
            images = convert_from_path(
                path,
                dpi=150,
                first_page=page_number + 1,
                last_page=page_number + 1,
                poppler_path=poppler_path,
                grayscale=True,
            )

            image = images[0]

            _log_memory(
                f"OCR page {page_number + 1}: image rendered"
            )

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

            image.close()
            del image, images
            gc.collect()

            _log_memory(
                f"OCR page {page_number + 1}: image released"
            )

        if not ocr_documents:
            raise ValueError(
                f"OCR did not extract text from {path}"
            )

        print(
            f"OCR extracted text from "
            f"{len(ocr_documents)} pages."
        )

        _log_memory("After OCR extraction")

        return ocr_documents

    except Exception as exc:
        raise RuntimeError(
            f"PDF text extraction and OCR both failed "
            f"for {path}: {exc}"
        ) from exc


def load_pdf(path):
    _log_memory("Starting load_pdf")

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

                _log_memory("After loading PDF extraction cache")

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

    _log_memory("Before saving PDF extraction cache")

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

    _log_memory("After saving PDF extraction cache")

    return documents
