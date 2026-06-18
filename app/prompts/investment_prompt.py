def build_investment_prompt(
    company_data,
    metrics,
    news_sentiment,
    risk_analysis
):

    return f"""
You are a professional investment analyst.

Company:
{company_data}

Metrics:
{metrics}

News Sentiment:
{news_sentiment}

Risk Analysis:
{risk_analysis}

Generate:

1. Recommendation
(BUY / HOLD / SELL)

2. Confidence Score
(0-100)

3. Reasoning

Keep it concise.
"""