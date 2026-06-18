from langgraph.graph import StateGraph, END

from app.graph.state import FinancialState

from app.services.yahoo_finance import get_company_data
from app.agents.metrics_agent import evaluate_metrics
from app.agents.news_agent import analyze_news
from app.services.llm_service import generate_analysis
from app.prompts.company_prompt import build_company_prompt
from app.agents.risk_agent import analyze_risk
from app.agents.investment_agent import analyze_investment


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

def final_analysis_node(
    state: FinancialState
):

    prompt = build_company_prompt(
        state["company_data"],
        state["metrics"],
        state["news"]
    )

    analysis = generate_analysis(
        prompt
    )

    return {
        "analysis": analysis
    }


builder = StateGraph(
    FinancialState
)

builder.add_node(
    "company",
    company_node
)

builder.add_node(
    "metrics",
    metrics_node
)

builder.add_node(
    "news",
    news_node
)

builder.add_node(
    "investment",
    investment_node
)

builder.add_node(
    "risk",
    risk_node
)

builder.add_node(
    "final_analysis",
    final_analysis_node
)

builder.set_entry_point(
    "company"
)

builder.add_edge(
    "company",
    "metrics"
)

builder.add_edge(
    "metrics",
    "news"
)

builder.add_edge(
    "news",
    "risk"
)

builder.add_edge(
    "risk",
    "investment"
)

builder.add_edge(
    "investment",
    "final_analysis"
)

builder.add_edge(
    "final_analysis",
    END
)

financial_graph = builder.compile()