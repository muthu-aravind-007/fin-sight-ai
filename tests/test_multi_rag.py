from app.agents.multi_rag_agent import (
    analyze_multiple_transcripts
)

documents = [
    {
        "pdf_path": "data/transcripts/nvda_q1_2027.pdf",
        "company": "NVDA",
        "quarter": "Q1 2027"
    },
    {
        "pdf_path": "data/transcripts/nvda_q2_2026.pdf",
        "company": "NVDA",
        "quarter": "Q2 2026"
    },
    {
        "pdf_path": "data/transcripts/msft_q3_2026.pdf",
        "company": "MSFT",
        "quarter": "Q3 2026"
    }
]

result = analyze_multiple_transcripts(
    documents,
    "What are Microsoft's AI opportunities?"
)

print("\nANSWER:\n")
print(
    result["answer"]
)

print("\nCONTEXT:\n")
print(
    result["context"][:1000]
)