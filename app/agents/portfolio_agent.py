from app.services.yahoo_finance import get_company_data
from app.agents.metrics_agent import evaluate_metrics
from app.prompts.portfolio_prompt import build_portfolio_prompt
from app.services.llm_service import generate_analysis

def analyze_portfolio(tickers):

    companies = []
    total_score = 0

    sectors = {}

    for ticker in tickers:

        company = get_company_data(
            ticker.strip()
        )

        metrics = evaluate_metrics(
            company
        )

        companies.append({
            "ticker": ticker,
            "company": company,
            "metrics": metrics
        })

        total_score += metrics["score"]

        sector = company["sector"]

        sectors[sector] = (
            sectors.get(sector, 0) + 1
        )

    average_score = round(
        total_score / len(companies),
        2
    )

    sector_count = len(sectors)

    if sector_count >= 5:
        diversification_score = 10

    elif sector_count == 4:
        diversification_score = 8

    elif sector_count == 3:
        diversification_score = 6

    elif sector_count == 2:
        diversification_score = 4

    else:
        diversification_score = 2

    sector_percentages = {}

    for sector, count in sectors.items():

        sector_percentages[sector] = round(
            (count / len(companies)) * 100,
            2
        )

    prompt = build_portfolio_prompt(
        companies,
        average_score,
        sector_percentages
    )

    analysis = generate_analysis(
        prompt
    )

    return {
        "companies": companies,
        "average_score": average_score,
        "diversification_score": diversification_score,
        "sectors": sector_percentages,
        "analysis": analysis
    }