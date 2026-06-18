from app.services.news_service import get_company_news
from app.services.llm_service import generate_analysis

from app.prompts.news_sentiment_prompt import (
    build_news_sentiment_prompt
)


def analyze_news(company_name):

    news = get_company_news(
        company_name
    )

    headlines = [
        item["title"]
        for item in news
    ]

    prompt = build_news_sentiment_prompt(
        company_name,
        headlines
    )

    sentiment = generate_analysis(
        prompt
    )

    return {
        "news": news,
        "sentiment": sentiment
    }