
def build_company_prompt(
    company_data,
    metrics,
    news,
    risk_analysis,
    investment_analysis,
):
    market_cap_value = company_data.get("market_cap")
    revenue_value = company_data.get("revenue")
    pe_ratio_value = company_data.get("pe_ratio")

    market_cap = (
        f"${market_cap_value / 1_000_000_000_000:.2f} Trillion"
        if market_cap_value is not None
        else "N/A"
    )

    revenue = (
        f"${revenue_value / 1_000_000_000:.2f} Billion"
        if revenue_value is not None
        else "N/A"
    )

    pe_ratio = (
        f"{pe_ratio_value:.2f}"
        if pe_ratio_value is not None
        else "N/A"
    )

    return f"""
You are a professional financial analyst.
Produce a balanced, evidence-based company report.

COMPANY INFORMATION

Name: {company_data.get("name") or "N/A"}
Sector: {company_data.get("sector") or "N/A"}
Industry: {company_data.get("industry") or "N/A"}

Market Cap: {market_cap}
Revenue: {revenue}
PE Ratio: {pe_ratio}

FINANCIAL METRICS

Score: {metrics["score"]}/6
Valuation: {metrics["valuation"]}
Growth: {metrics["growth"]}
Risk: {metrics["risk"]}

Metric Insights:
{metrics["insights"]}

RECENT NEWS

{news}

SPECIALIST RISK ANALYSIS

{risk_analysis}

SPECIALIST INVESTMENT ANALYSIS

{investment_analysis}


YOUR TASK

Synthesize all the information above into one coherent,
complete financial report.

Use these exact sections:

1. Company Overview
Summarize the company's business, sector, and key financial figures.

2. Financial Health Assessment
Explain the supplied metrics, valuation, growth, and financial
strengths or weaknesses.

3. Positive Signals
Identify the strongest supporting evidence from the metrics
and recent news.

4. Key Risks
Summarize the most material risks from the specialist risk
analysis. Explain their potential implications without repeating
every risk category verbatim.

5. Investment Outlook
Present the specialist investment recommendation and confidence
score if provided. Explain the supporting evidence, opposing
signals, and important uncertainties.

6. Final Rating
Choose Bullish, Neutral, or Bearish based on the combined
evidence. Explain briefly why this rating is appropriate and
what could change the outlook.


REQUIREMENTS

- Complete all six sections. Never omit a section.
- Target 450–650 words. Prefer concise paragraphs and bullet points.
- Use only supplied evidence. Never invent financial facts.
- Distinguish reported data from AI-generated interpretations.
- Explain meaningful disagreements between metrics, news, risk,
  and investment analysis.
- Preserve the specialist recommendation and confidence score
  when provided. Explain any disagreement.
- Avoid repeating the same facts and risks across sections.
- Do not assume positive news guarantees future performance.
- State important uncertainties and evidence limitations.
- Section 6 must give a clear Bullish, Neutral, or Bearish rating,
  its main rationale, and what could change the outlook.
- End with a complete conclusion. Never end mid-sentence.
"""
