import streamlit as st
import requests
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="FinSight AI",
    layout="wide"
)

st.title("📈 FinSight AI")
st.caption(
    "AI-Powered Financial Intelligence Platform"
)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Company Analysis",
        "⚔️ Company Comparison",
        "📄 Earnings Analyzer",
        "📊 Portfolio Analyzer"
    ]
)

with tab1:

    ticker = st.text_input(
        "Enter Stock Ticker",
        "NVDA",
        key="company_analysis"
    )

    if st.button(
        "Analyze",
        key="analyze_company"
    ):

        with st.spinner("Analyzing company..."):

            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={
                    "ticker": ticker
                }
            )

            result = response.json()

            company = result["company_data"]
            metrics = result["metrics"]

            stock = yf.Ticker(ticker)

            history = stock.history(
                period="6mo"
            )

            st.subheader(
                "📈 Stock Price Trend (6 Months)"
            )

            st.line_chart(
                history["Close"]
            )

            st.subheader(
                company["name"]
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Sector",
                company["sector"]
            )

            col2.metric(
                "P/E Ratio",
                round(
                    company["pe_ratio"],
                    2
                )
            )

            col3.metric(
                "Market Cap",
                f"${company['market_cap']/1e12:.2f}T"
            )

            st.subheader(
                "🎯 AI Investment Recommendation"
            )

            st.markdown(
                result["investment_analysis"]
            )

            st.subheader(
                "📊 Financial Analysis"
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Score",
                f"{metrics['score']}/6"
            )

            col2.metric(
                "Valuation",
                metrics["valuation"]
            )

            col3.metric(
                "Growth",
                metrics["growth"]
            )

            col4.metric(
                "Risk",
                metrics["risk"]
            )

            for insight in metrics["insights"]:
                st.success(insight)

            st.subheader(
                "📰 Latest News"
            )

            st.subheader(
                "🧠 News Sentiment"
            )

            st.markdown(
                result["news_sentiment"]
            )

            st.subheader(
                "⚠️ Risk Analysis"
            )

            st.markdown(
                result["risk_analysis"]
            )

            st.subheader(
                "📰 Latest News"
            )

            for item in result["news"]:

                st.markdown(
                    f"- [{item['title']}]({item['link']})"
                )

            st.subheader(
                "🤖 AI Investment Analysis"
            )

            st.markdown(
                result["analysis"]
            )

with tab2:

    st.subheader(
        "🏆 Company Comparison"
    )

    ticker1 = st.text_input(
        "Company 1",
        "NVDA",
        key="compare_1"
    )

    ticker2 = st.text_input(
        "Company 2",
        "AMD",
        key="compare_2"
    )

    if st.button(
        "Compare",
        key="compare_button"
    ):

        with st.spinner(
            "Comparing companies..."
        ):

            response = requests.post(
                "http://127.0.0.1:8000/compare",
                json={
                    "ticker1": ticker1,
                    "ticker2": ticker2
                }
            )

            result = response.json()

            company1 = result["company1"]
            company2 = result["company2"]

            metrics1 = result["metrics1"]
            metrics2 = result["metrics2"]

            st.subheader(
                f"{company1['name']} vs {company2['name']}"
            )

            comparison_data = {
                "Metric": [
                    "Market Cap",
                    "Revenue",
                    "P/E Ratio",
                    "Score",
                    "Growth",
                    "Risk"
                ],
                company1["name"]: [
                    f"${company1['market_cap']/1e12:.2f}T",
                    f"${company1['revenue']/1e9:.2f}B",
                    round(company1["pe_ratio"], 2),
                    metrics1["score"],
                    metrics1["growth"],
                    metrics1["risk"]
                ],
                company2["name"]: [
                    f"${company2['market_cap']/1e12:.2f}T",
                    f"${company2['revenue']/1e9:.2f}B",
                    round(company2["pe_ratio"], 2),
                    metrics2["score"],
                    metrics2["growth"],
                    metrics2["risk"]
                ]
            }

            st.table(
                comparison_data
            )

            st.subheader(
                "🤖 AI Comparison Analysis"
            )

            st.markdown(
                result["analysis"]
            )

with tab3:

    st.subheader(
        "📄 Earnings Call Analyzer"
    )

    transcript = st.text_area(
        "Paste Earnings Call Transcript",
        height=300
    )

    if st.button(
        "Analyze Earnings",
        key="earnings_button"
    ):

        with st.spinner(
            "Analyzing earnings call..."
        ):

            response = requests.post(
                "http://127.0.0.1:8000/earnings",
                json={
                    "transcript": transcript
                }
            )

            result = response.json()

            st.subheader(
                "📄 Earnings Analysis"
            )

            st.markdown(
                result["analysis"]
            )

with tab4:

    st.header(
        "📊 Portfolio Analyzer"
    )

    tickers = st.text_input(
        "Enter Tickers (comma separated)",
        "NVDA,AAPL,AMD"
    )

    if st.button(
        "Analyze Portfolio",
        key="portfolio_button"
    ):

        with st.spinner(
            "Analyzing portfolio..."
        ):

            response = requests.post(
                "http://127.0.0.1:8000/portfolio",
                json={
                    "tickers": tickers.split(",")
                }
            )

            result = response.json()

            col1, col2 = st.columns(2)

            col1.metric(
                "Portfolio Score",
                result["average_score"]
            )

            col2.metric(
                "Diversification Score",
                f"{result['diversification_score']}/10"
            )

            st.subheader(
                "📊 Sector Allocation"
            )

            sector_data = result["sectors"]

            sector_df = pd.DataFrame(
                sector_data.items(),
                columns=[
                    "Sector",
                    "Allocation %"
                ]
            )

            st.bar_chart(
                sector_df.set_index(
                    "Sector"
                )
            )

            st.subheader(
                "🤖 AI Portfolio Analysis"
            )

            st.markdown(
                result["analysis"]
            )