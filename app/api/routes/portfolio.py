from fastapi import APIRouter

from app.agents.portfolio_agent import (
    analyze_portfolio
)

router = APIRouter()


@router.post("/portfolio")
def portfolio(data: dict):

    tickers = data["tickers"]

    return analyze_portfolio(
        tickers
    )