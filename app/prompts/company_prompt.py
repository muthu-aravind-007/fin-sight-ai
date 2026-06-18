def build_company_prompt(
    company_data,
    metrics,
    news
):

    market_cap = (
        company_data["market_cap"] / 1_000_000_000_000
    )

    revenue = (
        company_data["revenue"] / 1_000_000_000
    )

    return f"""
You are a professional financial analyst.

Company Information

Name: {company_data["name"]}
Sector: {company_data["sector"]}
Industry: {company_data["industry"]}

Market Cap: ${market_cap:.2f} Trillion
Revenue: ${revenue:.2f} Billion
PE Ratio: {company_data["pe_ratio"]:.2f}

Financial Analysis

Score: {metrics["score"]}/6
Valuation: {metrics["valuation"]}
Growth: {metrics["growth"]}
Risk: {metrics["risk"]}

Insights:
{metrics["insights"]}

Recent News:
{news}

Generate:

1. Company Overview

2. Financial Health Assessment

3. Positive Signals

4. Risks

5. Investment Outlook

6. Final Rating
(Bullish / Neutral / Bearish)

Keep the response concise and professional.
"""