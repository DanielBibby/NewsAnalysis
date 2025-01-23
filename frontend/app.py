import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

from utils import create_dashboard

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.src.analysis_chain.chain import BaseAnalysisChain
from backend.src.news_finder.finder import APIException

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")

st.set_page_config(layout="wide")

st.title("News Sentiment and Stock Analysis 🧐")

st.markdown(
    """
    This app provides a simple interface to see how the sentiment of news articles about a company has changed over
    the last week or month. Additionally, it retrieves and displays stock price data for the selected company.
    
    Note, the free plan of NewsAPI restricts API calls to 100 articles, so if you enter a prominant company or entity,
    do not expect accurate results as articles used for analysis may only represent a small asmaple of news articles
    published.
    
    Alternatively, select 'Other' from the dropdown menu below to enter an entity of your choice, such as a celebrity, 
    football team, or anything else.

"""
)

st.divider()

st.markdown(
    """
**[Get your free API Key in 30 seconds](https://newsapi.org)**  

*Enter your API Key below. Leave blank if you've cloned the GitHub repository and followed README instructions.*
"""
)

api_key = st.text_input("API Key", type="password")

multi_company = st.selectbox(
    label="Select company here", options=["Tesla", "Meta", "JPMorgan", "Other"]
)

if multi_company == "Other":
    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input(label="Company")
    with col2:
        stock_code = st.text_input(label="Stock Ticker (Optional)")
else:
    stock_code = None
    company = None

time_frame = st.radio(
    label="How far back would you like to see", options=["One Week", "One Month"]
)


if st.button("Run Analysis"):
    with st.spinner("Running analysis ..."):
        # Map the selected time frame to a timedelta
        time_frame_map = {
            "One Week": timedelta(weeks=1),
            "One Month": timedelta(days=30),
        }

        # Set the date range
        end_date = datetime.now()
        start_date = end_date - time_frame_map[time_frame]

        # If stock_code is not provided, map the selected company to a default ticker
        default_tickers = {"Tesla": "TSLA", "Meta": "META", "JPMorgan": "JPM"}
        ticker = stock_code or default_tickers.get(multi_company, None)
        if ticker:
            ticker = ticker.upper()

        if company:
            chain = BaseAnalysisChain(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                company=company,
                api_key=api_key,
            )

        else:
            chain = BaseAnalysisChain(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                company=multi_company,
                api_key=api_key,
            )

        # run chain
        try:
            sentiments_df, total_articles = chain.run()
        except APIException as e:
            st.error(str(e))

        # Retrieve stock market data
        try:
            if ticker:
                stock_data = yf.download(ticker, start=start_date, end=end_date)

                if stock_data.empty:
                    st.warning(
                        "No data available for that ticker and time frame, make sure you spelt it correctly."
                    )
            else:
                stock_data = None
        except Exception as e:
            st.error(f"Error fetching stock data: {e}")

        st.subheader(
            f"Data for {multi_company if not company else company} and stock price of ({ticker}) based on 100 most popular "
            f"articles from the last {time_frame[4:].lower()}"
        )
        st.markdown(
            f"""
        #### Total Articles: {total_articles}
        **Reminder - At most, 100 of these articles are being analysed.**
        """
        )

        fig = create_dashboard(stock_data, ticker, sentiments_df)
        st.pyplot(fig)
