
import math

from app.prompts.risk_prompt import build_risk_prompt
from app.services.llm_service import generate_analysis


def has_valid_financial_data(company_data):

    for field in [
        "market_cap",
        "pe_ratio",
        "revenue"
    ]:
        value = company_data.get(field)

        if value is None:
            continue

        try:
            if math.isfinite(float(value)):
                return True
        except (TypeError, ValueError):
            continue

    return False


def has_usable_news_sentiment(news_sentiment):

    if not isinstance(news_sentiment, str):
        return False

    text = news_sentiment.strip().lower()

    if not text:
        return False

    unavailable_phrases = [
        "insufficient data",
        "no relevant news",
        "no usable news headlines"
    ]

    return not any(
        phrase in text
        for phrase in unavailable_phrases
    )


def analyze_risk(
    company_data,
    metrics,
    news_sentiment
):
    company_data = company_data or {}
    metrics = metrics or {}

    financial_evidence = has_valid_financial_data(
        company_data
    )

    news_evidence = has_usable_news_sentiment(
        news_sentiment
    )

    # No usable evidence: return a deterministic assessment.
    if not financial_evidence and not news_evidence:
        return (
            "Risk Assessment: Insufficient Data\n\n"
            "Valuation Risk: Unknown\n"
            "Business Risk: Unknown\n"
            "Competition Risk: Unknown\n"
            "Market Risk: Unknown\n"
            "Regulatory Risk: Unknown\n\n"
            "Risk Scores: N/A\n\n"
            "There is insufficient financial and news evidence "
            "to assess company-specific risks reliably."
        )

    prompt = build_risk_prompt(
        company_data,
        metrics,
        news_sentiment
    )

    return generate_analysis(prompt)
