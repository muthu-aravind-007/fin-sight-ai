from typing import TypedDict

class FinancialState(TypedDict):

    ticker: str

    company_data: dict

    metrics: dict

    news: list

    news_sentiment: str

    risk_analysis: str

    investment_analysis: str

    analysis: str