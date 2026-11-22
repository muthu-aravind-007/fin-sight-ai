import yfinance as yf


def get_company_data(ticker: str):

    stock = yf.Ticker(ticker)

    info = stock.info

    company_name = (
        info.get("longName")
        or info.get("shortName")
        or ticker.upper()
    )

    return {
        "name": company_name,
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "revenue": info.get("totalRevenue")
    }
