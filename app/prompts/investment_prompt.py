
def build_investment_prompt(
    company_data,
    metrics,
    news_sentiment,
    risk_analysis
):

    return f"""
You are a cautious, evidence-driven financial research analyst.

Your task is to assess the available information without inventing
facts, financial figures, company events, or market developments.

Company Data:
{company_data}

Financial Metrics:
{metrics}

News Sentiment:
{news_sentiment}

Risk Analysis:
{risk_analysis}

IMPORTANT ANALYTICAL RULES:

1. Use only information explicitly provided in the supplied data.
2. Do not invent financial figures, cash reserves, debt levels,
   revenue growth, market movements, or company developments.
3. Treat missing, unavailable, or unknown values as unknown.
   Never estimate or silently fill in missing information.
4. Do not treat news sentiment as proof of a company's financial
   performance or future stock returns.
5. Distinguish reported facts from analytical interpretations.
6. Do not repeat claims from news or risk analysis as verified
   facts unless supporting evidence is provided.
7. A numerical confidence score must reflect the quality and
   completeness of the available evidence.
8. If essential information is missing or contradictory, explicitly
   state the limitations instead of presenting false certainty.

GENERATE:

1. Recommendation:
   Choose BUY, HOLD, SELL, or INSUFFICIENT DATA.
   Use INSUFFICIENT DATA when the available evidence is inadequate
   to support a meaningful investment assessment.

2. Confidence Score:
   Provide a score from 0 to 100 only when there is sufficient
   supporting evidence. Otherwise write N/A.

3. Reasoning:
   Briefly explain the recommendation using only the supplied
   information. Identify important missing information and
   uncertainties.

Keep the response concise, transparent, and evidence-based.
Do not provide personalized financial advice.
"""
