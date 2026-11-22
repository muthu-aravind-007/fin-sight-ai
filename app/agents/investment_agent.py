
import math

from app.services.llm_service import generate_analysis

from app.prompts.investment_prompt import (
    build_investment_prompt
)


def has_valid_financial_data(company_data):
    required_fields = [
        "market_cap",
        "pe_ratio",
        "revenue",
    ]

    for field in required_fields:
        value = company_data.get(field)

        if value is None:
            return False

        try:
            if not math.isfinite(float(value)):
                return False
        except (TypeError, ValueError):
            return False

    return True


def analyze_investment(
    company_data,
    metrics,
    news_sentiment,
    risk_analysis
):
    if not has_valid_financial_data(company_data):
        return (
            "**Recommendation:** INSUFFICIENT DATA\n\n"
            "**Confidence Score:** N/A\n\n"
            "**Reasoning:** A reliable investment recommendation "
            "cannot be generated because essential financial data "
            "(market capitalization, P/E ratio, or revenue) is "
            "missing or invalid. No BUY or SELL recommendation "
            "should be inferred from incomplete financial information."
        )

    prompt = build_investment_prompt(
        company_data,
        metrics,
        news_sentiment,
        risk_analysis
    )

    return generate_analysis(prompt)
