
def build_multi_rag_prompt(
    context,
    question,
    comparison_mode=False,
    analysis_intent="general",
):
    intent_instructions = {
        "risks": """
Focus on material risks explicitly discussed by management.
Identify the companies that discuss each risk and cite the
supporting transcript evidence. Explain potential effects on
revenue, operating margins, cash flow, or return on investment.
Distinguish explicitly stated risks from analytical inferences.
Do not assume every company faces every risk.
""",
        "revenue_growth": """
Focus on revenue, sales growth, reported growth drivers,
and management's explanations for changes in performance.
Distinguish reported results from expectations and inferences.
Do not invent growth rates or attribute growth to unsupported causes.
""",
        "profitability": """
Focus on gross margin, operating margin, costs, expenses,
and profitability drivers. Explain reported changes and
potential implications using only the supplied evidence.
Do not confuse revenue growth with profit growth.
""",
        "cash_flow": """
Focus on operating cash flow, free cash flow, capital
expenditure, working capital, and cash requirements when
discussed. Explain potential implications without inventing
figures or treating cash flow and accounting profit as equivalent.
""",
        "ai_monetization": """
Focus on evidence of AI-related revenue, customer spending,
paid adoption, product monetization, and related investment.
Distinguish demonstrated financial results from product
announcements, customer interest, and management expectations.
Do not claim successful monetization without supporting evidence.
""",
        "management_outlook": """
Focus on management's forward-looking statements, guidance,
expectations, and stated uncertainties. Clearly distinguish
management's outlook from actual reported results.
""",
        "multi_topic": """
Address each topic requested by the user separately.
Organize findings around the actual question and avoid
letting one topic overshadow the others.
""",
        "general": """
Answer the user's specific question using the most relevant
evidence. Do not impose an unrelated analysis framework.
""",
    }

    intent_instruction = intent_instructions.get(
        analysis_intent,
        intent_instructions["general"],
    )

    if comparison_mode:
        output_format = """
## Direct Answer
Answer the user's specific question directly.

## Key Evidence
Identify the relevant companies, quarters, pages, and
exact Source IDs. Include supporting figures or passages.

## Cross-Company Analysis
Compare the companies on the requested topic.
Explain similarities, differences, and missing evidence.
Do not force every company into every finding.

## Financial Implications
Explain supported financial implications where relevant.
Distinguish management statements from analytical inferences.

## Limitations
Identify where evidence is insufficient. Missing evidence
does not establish that a company has no such risk or issue.
"""
    else:
        output_format = """
## Direct Answer
Answer the user's question directly.

## Key Evidence
Present the most relevant transcript evidence with Source IDs.

## Analysis
Explain the supported business and financial implications.
Separate management statements from analytical inferences.

## Limitations
Identify relevant information unavailable in the supplied context.
"""

    return f"""
You are a financial transcript research assistant.

Answer the user's exact question using ONLY the supplied
transcript context. Never replace the requested topic with
an unrelated financial analysis task.

Question:
{question}

Analysis intent:
{analysis_intent}

Intent-specific instructions:
{intent_instruction}

Transcript Context:
{context}

Rules:
1. Use only the supplied transcript context.
2. Cite material factual claims using exact Source IDs.
3. Never invent facts, figures, risks, or management statements.
4. Separate management's statements from your inferences.
5. Do not assume all companies face the same risks.
6. Do not treat missing evidence as evidence of no risk.
7. For cross-company questions, use relevant evidence from
   each company where available.
8. Explain when the supplied evidence is insufficient.
9. Follow the user's requested topic and deliverables.
10. Do not provide investment recommendations or valuation claims.
11. Keep the answer under 350 words.
12. Follow the intent-specific instructions when relevant.
13. If the user's explicit question conflicts with a broad
    intent label, prioritize the user's explicit question.

Required output format:
{output_format}
"""
