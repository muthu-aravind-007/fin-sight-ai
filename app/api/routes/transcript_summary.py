from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.transcript_summary_agent import (
    summarize_transcript
)

router = APIRouter()


class TranscriptSummaryRequest(
    BaseModel
):
    pdf_path: str


@router.post(
    "/transcript-summary"
)
def transcript_summary(
    request: TranscriptSummaryRequest
):

    return summarize_transcript(
        request.pdf_path
    )