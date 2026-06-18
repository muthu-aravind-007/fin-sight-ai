def build_news_sentiment_prompt(
    company_name,
    headlines
):

    headlines_text = "\n".join(headlines)

    return f"""
You are a financial news analyst.

Company:
{company_name}

News Headlines:
{headlines_text}

Analyze the news and generate:

1. Positive News

2. Negative News

3. Neutral News

4. Overall Sentiment
(Bullish / Neutral / Bearish)

5. Sentiment Score
(0-100)

6. Key Risks

7. Conclusion

Use only the provided headlines.
Respond only in English.
"""