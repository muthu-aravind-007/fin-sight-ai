
import math


def format_financial_value(value, divisor=1, suffix=""):
    if value is None:
        return "N/A"

    try:
        numeric_value = float(value)

        if not math.isfinite(numeric_value):
            return "N/A"

        return f"${numeric_value / divisor:.2f}{suffix}"

    except (TypeError, ValueError):
        return "N/A"


def build_company_prompt(
    company_data,
    metrics,
    news,
    risk_analysis,
    investment_analysis,
):
    market_cap = format_financial_value(
        company_data.get("market_cap"),
        1_000_000_000_000,
        " Trillion"
    )

    revenue = format_financial_value(
        company_data.get("revenue"),
        1_000_000_000,
        " Billion"
    )

    pe_ratio_value = company_data.get("pe_ratio")

    try:
        pe_numeric = float(pe_ratio_value)

        pe_ratio = (
            f"{pe_numeric:.2f}"
            if math.isfinite(pe_numeric)
            else "N/A"
        )
    except (TypeError, ValueError):
        pe_ratio = "N/A"

    metrics = metrics or {}

    return f"""
You are a cautious, professional financial research analyst.

Your responsibility is to produce a balanced report based only
on the information supplied below.

Do not invent financial facts, company developments, market events,
regulatory investigations, or supporting evidence.

COMPANY INFORMATION

Name: {company_data.get("name") or "N/A"}
Sector: {company_data.get("sector") or "N/A"}
Industry: {company_data.get("industry") or "N/A"}

Market Capitalization: {market_cap}
Revenue: {revenue}
P/E Ratio: {pe_ratio}

FINANCIAL METRICS

Score: {metrics.get("score", "N/A")}/6
Valuation: {metrics.get("valuation", "Unknown")}
Growth: {metrics.get("growth", "Unknown")}
Risk: {metrics.get("risk", "Unknown")}

Metric Insights:
{metrics.get("insights", [])}

RECENT NEWS HEADLINES

{news}

SPECIALIST RISK ANALYSIS

{risk_analysis}

SPECIALIST INVESTMENT ANALYSIS

{investment_analysis}

CRITICAL EVIDENCE AND RELIABILITY RULES

1. Treat N/A, Unknown, missing, and unavailable values as
   unavailable information. Never estimate or invent replacements.

2. Missing financial information does not prove that a company
   is financially weak or financially strong.

3. Do not claim that the company has strong cash reserves,
   low debt, improving margins, or healthy cash flow unless
   supporting figures are explicitly supplied.

4. News headlines are not independently verified evidence.
   Do not present allegations, investigations, lawsuits,
   leadership changes, or market events as confirmed facts
   based solely on headlines.

5. Specialist risk and investment outputs are AI-generated
   assessments, not independently verified facts.

6. Distinguish supplied financial data, reported news,
   analytical interpretations, and unknown information.

7. Do not invent positive signals or company-specific risks
   merely to fill a report section.

8. If the specialist investment analysis says
   INSUFFICIENT DATA, do not replace it with BUY, HOLD, or SELL.

9. Do not create a numerical confidence score if the specialist
   analysis does not provide a valid supporting score.

10. If essential financial information is missing, explain
    which parts of the financial assessment cannot be completed.

YOUR TASK

Synthesize the supplied information into one coherent report.

Use these exact sections:

1. Company Overview

Summarize the company's available business information,
sector, industry, and supplied financial figures.
Identify missing company information.

2. Financial Health Assessment

Explain the available financial metrics, valuation, growth,
and risk indicators.

Clearly identify unavailable financial information.
Do not infer financial strength from missing metrics.

3. Positive Signals

Identify positive signals supported by the supplied information.
Do not invent positive evidence.

4. Key Risks

Summarize the material risks in the specialist risk analysis.
Separate supported company-specific information from
general industry risks and unverified claims.

5. Investment Outlook

Present the specialist investment assessment when supported.
Explain its reasoning, opposing signals, and limitations.

If the specialist recommendation is INSUFFICIENT DATA,
preserve that conclusion and explain why.

6. Final Rating

Choose one:

- Bullish
- Neutral
- Bearish
- Insufficient Data

Use Insufficient Data when the available evidence is inadequate
to support a meaningful investment rating.

Do not force a directional rating simply to complete the report.

REQUIREMENTS

- Complete all six sections.
- Prefer concise paragraphs and bullet points.
- Use only supplied evidence.
- Distinguish financial facts from AI interpretations.
- Explain meaningful disagreements between specialist outputs.
- Do not override an INSUFFICIENT DATA recommendation.
- State important uncertainties and evidence limitations.
- Never present unsupported claims as verified facts.
- End with a complete conclusion.
"""
