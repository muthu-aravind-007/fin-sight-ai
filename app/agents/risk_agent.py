
from app.prompts.risk_prompt import build_risk_prompt
from app.services.llm_service import generate_analysis


def analyze_risk(
    company_data,
    metrics,
    news_sentiment
):
    company_data = company_data or {}
    metrics = metrics or {}

    has_financial_data = any(
        company_data.get(field) is not None
        for field in [
            "market_cap",
            "pe_ratio",
            "revenue"
        ]
    )

    has_news_evidence = (
        isinstance(news_sentiment, str)
        and "insufficient data" not in news_sentiment.lower()
        and "no relevant news" not in news_sentiment.lower()
        and bool(news_sentiment.strip())
    )

    if not has_financial_data and not has_news_evidence:
        return (
            "Risk Assessment: Insufficient Data\n\n"
            "Valuation Risk: Unknown\n"
            "Business Risk: Unknown\n"
            "Competition Risk: Unknown\n"
            "Market Risk: Unknown\n"
            "Regulatory Risk: Unknown\n\n"
            "There is insufficient financial and news evidence "
            "to assess company-specific risks reliably."
        )

    prompt = build_risk_prompt(
        company_data,
        metrics,
        news_sentiment
    )

    return generate_analysis(prompt)
