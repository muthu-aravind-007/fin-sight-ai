
def build_company_prompt(
    company_data,
    metrics,
    news,
    risk_analysis,
    investment_analysis,
):
    market_cap = (
        company_data["market_cap"] / 1_000_000_000_000
    )

    revenue = (
        company_data["revenue"] / 1_000_000_000
    )

    return f"""
You are a professional financial analyst.
Produce a balanced, evidence-based company report.

COMPANY INFORMATION

Name: {company_data["name"]}
Sector: {company_data["sector"]}
Industry: {company_data["industry"]}

Market Cap: ${market_cap:.2f} Trillion
Revenue: ${revenue:.2f} Billion
PE Ratio: {company_data["pe_ratio"]:.2f}

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