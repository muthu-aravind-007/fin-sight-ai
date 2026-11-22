import time
import math

from langgraph.graph import StateGraph, START, END

from app.graph.state import FinancialState

from app.services.yahoo_finance import get_company_data
from app.agents.metrics_agent import evaluate_metrics
from app.agents.news_agent import analyze_news
from app.services.llm_service import generate_analysis
from app.prompts.company_prompt import build_company_prompt
from app.agents.risk_agent import analyze_risk
from app.agents.investment_agent import analyze_investment

def timed_node(name, fn, state):
    start = time.perf_counter()

    try:
        return fn(state)
    finally:
        elapsed = time.perf_counter() - start
        print(f"[LATENCY] {name}: {elapsed:.2f}s")

def company_node(state: FinancialState):

    company_data = get_company_data(
        state["ticker"]
    )

    return {
        "company_data": company_data
    }


def metrics_node(state: FinancialState):

    metrics = evaluate_metrics(
        state["company_data"]
    )

    return {
        "metrics": metrics
    }


def news_node(state: FinancialState):

    news_result = analyze_news(
        state["company_data"]["name"]
    )

    return {
        "news": news_result["news"],
        "news_sentiment": news_result["sentiment"]
    }


def investment_node(state: FinancialState):

    return {
        "investment_analysis":
        analyze_investment(
            state["company_data"],
            state["metrics"],
            state["news_sentiment"],
            state["risk_analysis"]
        )
    }

def risk_node(state):

    return {
        "risk_analysis": analyze_risk(
            state["company_data"],
            state["metrics"],
            state["news_sentiment"]
        )
    }


def final_analysis_node(state: FinancialState):
    company_data = state["company_data"]
    metrics = state["metrics"]

    # Keep specialist findings concise while preserving
    # their recommendations, scores, and key evidence.
    risk = " ".join(
        str(state["risk_analysis"]).split()
    )[:1200]

    investment = " ".join(
        str(state["investment_analysis"]).split()
    )[:1200]

    # Keep the five most recent headlines.
    news_items = state["news"]

    if isinstance(news_items, list):
        headlines = []

        for item in news_items[:5]:
            if isinstance(item, dict):
                title = item.get("title", "")
                if title:
                    headlines.append(str(title))
            else:
                headlines.append(str(item))

        news = "\n".join(headlines)
    else:
        news = str(news_items)

    news = " ".join(news.split())[:800]


    # --------------------------------------------------
    # Deterministic fallback for insufficient evidence
    # --------------------------------------------------

    required_fields = [
        "market_cap",
        "pe_ratio",
        "revenue",
    ]

    has_complete_financial_data = True

    for field in required_fields:
        value = company_data.get(field)

        try:
            if value is None or not math.isfinite(float(value)):
                has_complete_financial_data = False
                break
        except (TypeError, ValueError):
            has_complete_financial_data = False
            break

    has_news_evidence = bool(news.strip())

    if not has_complete_financial_data and not has_news_evidence:

        company_name = (
            company_data.get("name")
            or state["ticker"]
        )

        analysis = f"""
# 1. Company Overview

**{company_name}**

Company identification is available, but sufficient financial
and news information is unavailable to produce a reliable
company research assessment.

# 2. Financial Health Assessment

- Market Capitalization: N/A
- P/E Ratio: N/A
- Revenue: N/A
- Valuation: Unknown
- Revenue Scale: Unknown
- Risk: Unknown

Financial health cannot be reliably assessed without the
necessary financial information.

# 3. Positive Signals

No sufficiently supported positive financial or news signals
are available for evaluation.

This does not mean that the company has no positive attributes.

# 4. Key Risks

Company-specific risks cannot be reliably established from
the available information.

Valuation, business, competition, market, and regulatory risks
remain unassessed.

# 5. Investment Outlook

**Recommendation: INSUFFICIENT DATA**

**Confidence Score: N/A**

The available evidence is inadequate to support a meaningful
investment recommendation. A BUY, HOLD, or SELL conclusion
should not be inferred.

Additional verified financial information and relevant news
evidence are required.

# 6. Final Rating

**Insufficient Data**

A directional investment rating cannot be justified using
the currently available evidence.

The outlook can be reassessed when reliable financial figures
and relevant supporting information become available.
"""

        return {
            "analysis": analysis.strip()
        }


    prompt = build_company_prompt(
        company_data,
        metrics,
        news,
        risk,
        investment,
    )

    analysis = generate_analysis(
        prompt,
        num_predict=1000,
    )

    return {
        "analysis": analysis
    }

builder = StateGraph(
    FinancialState
)

builder.add_node(
    "company",
    lambda state: timed_node(
        "company", company_node, state
    )
)

builder.add_node(
    "metrics",
    lambda state: timed_node(
        "metrics", metrics_node, state
    )
)

builder.add_node(
    "news",
    lambda state: timed_node(
        "news", news_node, state
    )
)

builder.add_node(
    "risk",
    lambda state: timed_node(
        "risk", risk_node, state
    )
)

builder.add_node(
    "investment",
    lambda state: timed_node(
        "investment", investment_node, state
    )
)

builder.add_node(
    "final_analysis",
    lambda state: timed_node(
        "final_analysis", final_analysis_node, state
    )
)

builder.add_edge(START, "company")
builder.add_edge("company", "metrics")
builder.add_edge("metrics", "news")
builder.add_edge("news", "risk")
builder.add_edge("risk", "investment")
builder.add_edge("investment", "final_analysis")
builder.add_edge("final_analysis", END)

financial_graph = builder.compile()
