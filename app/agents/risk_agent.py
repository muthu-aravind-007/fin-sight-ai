from app.prompts.risk_prompt import build_risk_prompt
from app.services.llm_service import generate_analysis


def analyze_risk(
    company_data,
    metrics,
    news_sentiment
):

    prompt = build_risk_prompt(
        company_data,
        metrics,
        news_sentiment
    )

    return generate_analysis(
        prompt
    )