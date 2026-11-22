import logging
import yfinance as yf

logger = logging.getLogger(__name__)


def get_company_data(ticker: str):

    ticker = ticker.strip().upper()

    result = {
        "name": ticker,
        "sector": None,
        "industry": None,
        "market_cap": None,
        "pe_ratio": None,
        "revenue": None,
    }

    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}

        result.update({
            "name": (
                info.get("longName")
                or info.get("shortName")
                or ticker
            ),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "revenue": info.get("totalRevenue"),
        })

    except Exception as error:
        logger.warning(
            "Yahoo Finance data retrieval failed for %s: %s",
            ticker,
            error
        )

    return result
