from app.graph.workflow import financial_graph

def analyze_company(ticker):

    result = financial_graph.invoke(
        {
            "ticker": ticker
        }
    )

    return {
        "company_data": result["company_data"],
        "metrics": result["metrics"],
        "news": result["news"],
        "news_sentiment": result["news_sentiment"],
        "risk_analysis": result["risk_analysis"],
        "investment_analysis": result["investment_analysis"],
        "analysis": result["analysis"]
}