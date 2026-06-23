def build_transcript_summary_prompt(
    context
):

    return f"""
You are a professional financial analyst.

Analyze the earnings transcript below.

Transcript:

{context}

Generate:

1. Executive Summary

2. Bullish Signals

3. Bearish Signals

4. Key Risks

5. Future Outlook

Keep the response concise,
professional, and investor-focused.
"""