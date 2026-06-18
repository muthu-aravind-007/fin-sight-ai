def build_news_prompt(
    company_data,
    metrics,
    news
):

    return f"""
You are a professional financial analyst.

Company Information:
{company_data}

Financial Metrics Evaluation:
{metrics}

Recent News:
{news}

Generate:

1. Company Overview

2. Financial Health Assessment

3. Positive Signals

4. Risks

5. Investment Outlook

6. Final Rating
(Bullish, Neutral, Bearish)

Keep the analysis concise and professional.
"""