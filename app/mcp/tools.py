from .registry import mcp

import app.agents.company_agent as company_agent
import app.agents.comparison_agent as comparison_agent
import app.agents.portfolio_agent as portfolio_agent
import app.agents.news_agent as news_agent
import app.agents.metrics_agent as metrics_agent
import app.agents.multi_rag_agent as multi_rag_agent
import app.agents.earnings_rag_agent as earnings_rag_agent
import app.agents.transcript_summary_agent as transcript_summary_agent

@mcp.tool()
def company_analysis(ticker: str):
    return company_agent.analyze_company(ticker)

@mcp.tool()
def compare_companies(
    ticker1: str,
    ticker2: str
):
    return comparison_agent.compare_companies(
        ticker1,
        ticker2
    )

@mcp.tool()
def portfolio_analysis(
    tickers: list[str]
):
    return portfolio_agent.analyze_portfolio(
        tickers
    )

@mcp.tool()
def news_analysis(company: str):
    return news_agent.analyze_news(company)

@mcp.tool()
def metrics_analysis(ticker: str):
    company = company_agent.analyze_company(ticker)
    return metrics_agent.evaluate_metrics(
        company["company_data"]
    )

@mcp.tool()
def index_earnings_pdf(
    pdf_path: str,
    persist_directory: str
):
    return earnings_rag_agent.index_earnings_pdf(
        pdf_path,
        persist_directory
    )
    
@mcp.tool()
def query_earnings_pdf(
    question: str,
    persist_directory: str
): 
    return earnings_rag_agent.query_earnings_pdf(
        question,
        persist_directory
    )

@mcp.tool()
def summarize_transcript(
    pdf_path: str
):
    return transcript_summary_agent.summarize_transcript(
        pdf_path
    )

@mcp.tool()
def analyze_multiple_transcripts(
    documents,
    question
):
    return multi_rag_agent.analyze_multiple_transcripts(
        documents,
        question
    )
    
