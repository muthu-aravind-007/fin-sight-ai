import time

from app.services.news_service import get_company_news
from app.services.llm_service import generate_analysis
from app.prompts.news_sentiment_prompt import (
    build_news_sentiment_prompt
)


def analyze_news(company_name):

    # Measure external news retrieval
    start = time.perf_counter()

    news = get_company_news(company_name)

    print(
        f"[LATENCY] News retrieval: "
        f"{time.perf_counter() - start:.2f}s"
    )

    headlines = [
        item["title"]
        for item in news
    ]

    prompt = build_news_sentiment_prompt(
        company_name,
        headlines
    )

    # Measure LLM sentiment analysis
    start = time.perf_counter()

    sentiment = generate_analysis(prompt)

    print(
        f"[LATENCY] News sentiment LLM: "
        f"{time.perf_counter() - start:.2f}s"
    )

    return {
        "news": news,
        "sentiment": sentiment
    }
