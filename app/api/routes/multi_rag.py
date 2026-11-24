
import json
import os
import shutil
import tempfile

from pathlib import Path
from fastapi import UploadFile, File, Form, HTTPException
from fastapi import APIRouter

from app.agents.multi_rag_agent import (
    analyze_multiple_transcripts
)

router = APIRouter()

@router.post("/multi-rag/upload")
def multi_rag_upload(
    files: list[UploadFile] = File(...),
    documents: str = Form(...),
    question: str = Form(...),
):
    try:
        metadata = json.loads(documents)

        if not isinstance(metadata, list):
            raise ValueError("Documents must be a list.")

        if len(files) != len(metadata):
            raise ValueError(
                "Each uploaded PDF must have matching document details."
            )

        if not files:
            raise ValueError("Upload at least one PDF.")

        if not question.strip():
            raise ValueError("Enter a research question.")

        with tempfile.TemporaryDirectory() as temp_dir:
            processed_documents = []

            for index, (uploaded_file, details) in enumerate(
                zip(files, metadata)
            ):
                if Path(uploaded_file.filename or "").suffix.lower() != ".pdf":
                    raise ValueError("Only PDF files are supported.")

                company = str(details.get("company", "")).strip()
                quarter = str(details.get("quarter", "")).strip()

                if not company or not quarter:
                    raise ValueError(
                        "Every document needs a company and quarter."
                    )

                pdf_path = os.path.join(
                    temp_dir,
                    f"document_{index}.pdf",
                )

                with open(pdf_path, "wb") as destination:
                    shutil.copyfileobj(
                        uploaded_file.file,
                        destination,
                    )

                processed_documents.append({
                    "pdf_path": pdf_path,
                    "company": company,
                    "quarter": quarter,
                })

            return analyze_multiple_transcripts(
                processed_documents,
                question.strip(),
            )

    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        for uploaded_file in files:
            uploaded_file.file.close()
            
@router.post("/multi-rag")
def multi_rag(request: dict):

    result = analyze_multiple_transcripts(
        request["documents"],
        request["question"]
    )

    return result