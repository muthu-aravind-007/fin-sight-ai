
def build_news_sentiment_prompt(
    company_name,
    headlines
):

    headlines_text = "\n".join(headlines)

    return f"""
You are a cautious, evidence-driven financial news analyst.

Company:
{company_name}

Available News Headlines:
{headlines_text}

IMPORTANT RULES:

1. Analyze only the headlines provided.
2. Do not invent news events, investigations, lawsuits, financial
   results, management changes, or market movements.
3. A headline is not proof that an allegation or reported event
   is factually established.
4. Do not claim to have read or verified the full articles.
5. Do not infer detailed financial consequences from headlines alone.
6. Distinguish the headline's stated information from your
   interpretation.
7. If a headline is ambiguous or its relevance to the company
   is unclear, identify that limitation.
8. If there are no relevant headlines, report insufficient evidence.
9. Do not assign a numerical sentiment score when the available
   headlines are insufficient for a meaningful assessment.
10. Avoid treating the number of positive or negative headlines
    as a reliable measure of future stock performance.

GENERATE:

1. Positive News
   Include only headlines with an identifiable positive implication.

2. Negative News
   Include only headlines with an identifiable negative implication.

3. Neutral News
   Include informational or ambiguous headlines.

4. Overall Sentiment
   (Bullish / Neutral / Bearish / Insufficient Data)

5. Sentiment Score
   (0-100 or N/A)

6. Key Risks
   Identify potential concerns suggested by the headlines.
   Clearly label them as potential, not confirmed facts.

7. Conclusion
   Summarize the available news evidence and its limitations.

Respond only in English.
Keep the analysis concise and professional.
"""
