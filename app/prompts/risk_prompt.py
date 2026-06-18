def build_risk_prompt(
    company_data,
    metrics,
    news_sentiment
):

    return f"""
You are a professional equity risk analyst.

Company Information:
{company_data}

Financial Metrics:
{metrics}

News Sentiment:
{news_sentiment}

Analyze:

1. Valuation Risk
2. Business Risk
3. Competition Risk
4. Market Risk
5. Regulatory Risk

Provide:

Risk Level:
(Low / Medium / High)

Risk Score:
(1-10)

Key Risks:
- Risk 1
- Risk 2
- Risk 3

Keep the response concise.
"""