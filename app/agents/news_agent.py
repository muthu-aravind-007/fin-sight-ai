
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

    if not news:
        return {
            "news": [],
            "sentiment": (
                "Overall Sentiment: Insufficient Data\n\n"
                "Sentiment Score: N/A\n\n"
                "No relevant news headlines were available. "
                "A reliable news sentiment assessment cannot "
                "be generated."
            )
        }

    # Extract valid headlines and remove duplicates
    headlines = []
    seen_headlines = set()

    for item in news:

        if not isinstance(item, dict):
            continue

        title = item.get("title")

        if not isinstance(title, str):
            continue

        title = " ".join(title.split())

        if not title:
            continue

        normalized_title = title.casefold()

        if normalized_title in seen_headlines:
            continue

        seen_headlines.add(normalized_title)
        headlines.append(title)

    if not headlines:
        return {
            "news": news,
            "sentiment": (
                "Overall Sentiment: Insufficient Data\n\n"
                "Sentiment Score: N/A\n\n"
                "No usable news headlines were available."
            )
        }

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
