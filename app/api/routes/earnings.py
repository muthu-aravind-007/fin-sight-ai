from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.earnings_agent import (
    analyze_earnings
)

router = APIRouter()


class EarningsRequest(BaseModel):
    transcript: str


@router.post("/earnings")
def earnings(request: EarningsRequest):

    return analyze_earnings(
        request.transcript
    )