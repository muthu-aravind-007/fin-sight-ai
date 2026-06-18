def build_earnings_prompt(transcript):

    return f"""
You are a senior financial analyst.

IMPORTANT RULES:

- Respond only in English.
- Use ONLY information present in the transcript.
- Do NOT invent risks or opportunities.
- If information is not mentioned, write:
  "Not Mentioned".

Transcript:

{transcript}

Generate:

## Executive Summary

## Bullish Signals
List only signals explicitly mentioned.

## Bearish Signals
List only signals explicitly mentioned.

## Management Confidence Score
Give score from 1-10 and explain why.

## Future Outlook
Bullish / Neutral / Bearish

## Final Investment View
Buy / Hold / Sell

## Key Evidence
Quote the most important statements from the transcript.
"""