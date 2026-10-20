
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(path):
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

    print(f"Little or no selectable text found in {path}. Trying OCR...")

    try:
        import pytesseract
        from pdf2image import convert_from_path
        from langchain_core.documents import Document

        # Actual Tesseract executable path.
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        # Poppler executable directory.
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
