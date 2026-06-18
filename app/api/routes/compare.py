from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.comparison_agent import compare_companies

router = APIRouter()


class CompareRequest(BaseModel):
    ticker1: str
    ticker2: str


@router.post("/compare")
def compare(request: CompareRequest):

    return compare_companies(
        request.ticker1,
        request.ticker2
    )