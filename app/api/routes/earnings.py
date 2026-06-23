from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.earnings_agent import (
    analyze_earnings
)

from app.agents.earnings_rag_agent import (
    analyze_earnings_rag
)

router = APIRouter()


class EarningsRequest(BaseModel):
    transcript: str


class EarningsRAGRequest(BaseModel):
    pdf_path: str
    question: str


@router.post("/earnings")
def earnings(request: EarningsRequest):

    return analyze_earnings(
        request.transcript
    )


@router.post("/earnings-rag")
def earnings_rag(
    request: EarningsRAGRequest
):

    return analyze_earnings_rag(
        request.pdf_path,
        request.question
    )