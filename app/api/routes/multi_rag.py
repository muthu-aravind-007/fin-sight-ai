from fastapi import APIRouter

from app.agents.multi_rag_agent import (
    analyze_multiple_transcripts
)

router = APIRouter()


@router.post("/multi-rag")
def multi_rag(request: dict):

    result = analyze_multiple_transcripts(
        request["documents"],
        request["question"]
    )

    return result