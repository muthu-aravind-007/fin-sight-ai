
import re


def parse_question(question):
    result = {
        "quarters": [],
        "comparison_mode": False,
        "analysis_intent": "general",
    }

    q = question.lower()

    # Recognize quarter formats such as Q2 2026, Q2-FY2026,
    # Q2 FY2026, and Q2-2026.
    quarters = re.findall(
        r"\bQ([1-4])\s*[- ]?\s*(?:FY\s*)?(\d{4})\b",
        question,
        flags=re.IGNORECASE,
    )

    result["quarters"] = list(
        dict.fromkeys(
            f"Q{quarter} {year}"
            for quarter, year in quarters
        )
    )

    # Comparison scope: are multiple entities being compared?
    comparison_terms = [
        "compare",
        "comparison",
        "versus",
        "vs.",
        "differences between",
        "difference between",
        "across all",
        "across the companies",
        "across companies",
        "cross-company",
        "cross company",
        "between companies",
    ]

    result["comparison_mode"] = any(
        term in q for term in comparison_terms
    )

    # Analytical intent: what does the user want to analyze?
    intent_keywords = {
        "risks": [
            "risk",
            "risks",
            "risk factor",
            "financial risk",
            "uncertainty",
            "uncertainties",
        ],
        "revenue_growth": [
            "revenue growth",
            "sales growth",
            "revenue",
            "growth rate",
        ],
        "profitability": [
            "profitability",
            "operating margin",
            "gross margin",
            "net income",
            "profit margin",
        ],
        "cash_flow": [
            "cash flow",
            "free cash flow",
            "capital expenditure",
            "capex",
        ],
        "ai_monetization": [
            "ai monetization",
            "monetize ai",
            "monetization",
        ],
        "management_outlook": [
            "management outlook",
            "future outlook",
            "guidance",
            "forecast",
        ],
    }

    matched_intents = [
        intent
        for intent, keywords in intent_keywords.items()
        if any(keyword in q for keyword in keywords)
    ]

    if len(matched_intents) == 1:
        result["analysis_intent"] = matched_intents[0]
    elif len(matched_intents) > 1:
        result["analysis_intent"] = "multi_topic"

    return result
