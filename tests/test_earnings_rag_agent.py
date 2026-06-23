from app.agents.earnings_rag_agent import (
    analyze_earnings_rag
)

result = analyze_earnings_rag(
    "data/transcripts/nvda_q1_2027.pdf",
    "What did management say about AI demand?"
)

print(result["answer"])