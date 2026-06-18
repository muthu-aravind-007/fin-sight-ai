from app.services.yahoo_finance import get_company_data
from app.agents.metrics_agent import evaluate_metrics
from app.services.llm_service import generate_analysis


def compare_companies(ticker1, ticker2):

    company1 = get_company_data(ticker1)
    company2 = get_company_data(ticker2)

    metrics1 = evaluate_metrics(company1)
    metrics2 = evaluate_metrics(company2)

    prompt = f"""
Compare these two companies.

Company A:
{company1}

Metrics A:
{metrics1}

Company B:
{company2}

Metrics B:
{metrics2}

Answer:

1. Which company is financially stronger?
2. Which company is cheaper?
3. Which company has better growth potential?
4. Final recommendation.
"""

    analysis = generate_analysis(prompt)

    return {
        "company1": company1,
        "company2": company2,
        "metrics1": metrics1,
        "metrics2": metrics2,
        "analysis": analysis
    }