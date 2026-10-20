import re


CONCEPT_GROUPS = {
    "revenue": [
        "revenue", "sales", "turnover", "net sales",
        "year-over-year growth", "year-over-year change",
        "reported revenue", "comparable period",
    ],
    "profitability": [
        "profit", "profitability", "operating income",
        "operating margin", "gross margin", "net income",
        "earnings", "diluted earnings per share", "EPS",
    ],
    "cash_flow": [
        "cash flow", "operating cash flow",
        "free cash flow", "cash generation",
        "capital allocation", "liquidity",
    ],
    "guidance": [
        "guidance", "outlook", "forecast",
        "expectations", "forward-looking statements",
        "next quarter", "full-year outlook",
    ],
    "costs_and_investment": [
        "operating expenses", "capital expenditure",
        "capital expenditures", "capex", "R&D",
        "research and development", "cost structure",
        "infrastructure spending",
    ],
    "risk": [
        "risk factors", "uncertainties", "headwinds",
        "challenges", "regulatory risks",
        "supply constraints", "competition",
    ],
    "strategy": [
        "strategic priorities", "business strategy",
        "growth drivers", "competitive position",
        "market opportunity", "long-term plans",
    ],
    "segments": [
        "business segment", "segment revenue",
        "geographic revenue", "product revenue",
        "segment growth", "business unit performance",
    ],
    "customers_and_demand": [
        "customer demand", "customer adoption",
        "customer growth", "bookings", "backlog",
        "retention", "pricing", "sales volume",
    ],
    "ai_and_technology": [
        "artificial intelligence", "machine learning",
        "generative AI", "AI infrastructure",
        "cloud computing", "inference", "data centers",
        "Copilot", "automation", "technology investment",
    ],
    "operations": [
        "operational efficiency", "productivity",
        "capacity", "supply chain", "production",
        "delivery constraints", "utilization",
    ],
    "reporting_period": [
        "fiscal quarter", "fiscal year",
        "quarter ended", "reported period",
        "year-over-year comparison",
        "prior-year period",
    ],
}


def _normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def expand_query(question):
    """
    Expand financial-analysis questions using related concepts.

    Always preserves the original question. Adds relevant terms
    only when a concept group is detected.
    """
    normalized_question = _normalize(question)
    expansions = []

    for terms in CONCEPT_GROUPS.values():
        # Match a concept only if at least one term is present.
        if any(
            _normalize(term) in normalized_question
            for term in terms
        ):
            expansions.extend(terms)

    # Preserve order and avoid duplicate expansion terms.
    unique_expansions = list(dict.fromkeys(
        term for term in expansions
        if term not in normalized_question
    ))

    if not unique_expansions:
        return question

    return question + "\nRelated concepts: " + "; ".join(
        unique_expansions
    )
