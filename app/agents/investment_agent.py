from app.services.llm_service import generate_analysis

from app.prompts.investment_prompt import (
    build_investment_prompt
)


def analyze_investment(
    company_data,
    metrics,
    news_sentiment,
    risk_analysis
):

    prompt = build_investment_prompt(
        company_data,
        metrics,
        news_sentiment,
        risk_analysis
    )

    return generate_analysis(
        prompt
    )