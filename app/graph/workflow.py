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

    company_data = state["company_data"] or {}
    metrics = state["metrics"] or {}

    # Keep specialist findings concise.
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

                if isinstance(title, str) and title.strip():
                    headlines.append(title.strip())

            elif isinstance(item, str) and item.strip():
                headlines.append(item.strip())

        news = "\n".join(headlines)

    else:
        news = str(news_items or "")

    news = " ".join(news.split())[:800]

    # --------------------------------------------------
    # Validate essential financial information
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

    # --------------------------------------------------
    # Deterministic fallback for incomplete financial data
    # --------------------------------------------------

    if not has_complete_financial_data:

        company_name = (
            company_data.get("name")
            or state["ticker"]
        )

        def display_value(value, is_currency=True):

            if value is None:
                return "N/A"

            try:
                numeric_value = float(value)

                if not math.isfinite(numeric_value):
                    return "N/A"

                if is_currency:
                    return f"${numeric_value:,.0f}"

                return f"{numeric_value:.2f}"

            except (TypeError, ValueError):
                return "N/A"

        market_cap = display_value(
            company_data.get("market_cap")
        )

        revenue = display_value(
            company_data.get("revenue")
        )

        pe_ratio = display_value(
            company_data.get("pe_ratio"),
            is_currency=False
        )

        if news.strip():
            news_status = (
                "News headlines were retrieved. However, "
                "headline text is not independently verified "
                "and does not establish reported events as facts."
            )

            news_details = (
                f"\n\nAvailable headline text:\n{news}"
            )

        else:
            news_status = (
                "No usable news headlines were available."
            )

            news_details = ""

        analysis = f"""
# 1. Company Overview

**{company_name}**

Company identification is available, but one or more
essential financial metrics are missing or invalid.

Market Capitalization: {market_cap}
Revenue: {revenue}
P/E Ratio: {pe_ratio}

A complete financial research assessment cannot be
generated from the currently available financial data.

# 2. Financial Health Assessment

- Market Capitalization: {market_cap}
- P/E Ratio: {pe_ratio}
- Revenue: {revenue}
- Valuation: {metrics.get("valuation", "Unknown")}
- Growth: {metrics.get("growth", "Unknown")}
- Revenue Scale: {metrics.get("revenue_scale", "Unknown")}
- Risk: {metrics.get("risk", "Not Assessed")}

The available financial information is incomplete.
Missing values prevent a reliable assessment of overall
financial health.

Revenue scale does not establish revenue growth or
profitability. A P/E ratio alone does not establish
whether a stock is undervalued or overvalued.

# 3. Positive Signals

No complete set of financial indicators is available
to establish a reliable positive financial assessment.

This does not mean the company has no positive attributes.

# 4. Key Risks

Company-specific financial risks cannot be comprehensively
assessed with the available information.

Valuation, business, competition, market, and regulatory
risks should not be assigned unsupported conclusions.

**News Evidence**

{news_status}{news_details}

News headlines may identify topics for further verification,
but they should not be treated as confirmed events or
independent proof of company-specific risks.

# 5. Investment Outlook

**Recommendation: INSUFFICIENT DATA**

**Confidence Score: N/A**

The available financial evidence is inadequate to support
a reliable investment recommendation.

A BUY, HOLD, or SELL conclusion should not be inferred
from incomplete financial information.

Additional reliable financial data is required before
a meaningful investment assessment can be completed.

# 6. Final Rating

**Insufficient Data**

A directional investment rating cannot be justified
using the currently available financial evidence.

The assessment can be revisited when the missing
financial information becomes available.
"""

        return {
            "analysis": analysis.strip()
        }

    # --------------------------------------------------
    # Generate final report when financial data is complete
    # --------------------------------------------------

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
