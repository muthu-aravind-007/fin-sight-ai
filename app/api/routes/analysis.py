from fastapi import APIRouter

from app.models.schemas import TickerRequest
from app.agents.company_agent import analyze_company

router = APIRouter()

@router.post("/analyze")
def analyze(request: TickerRequest):

    return analyze_company(request.ticker)