import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

from utils import create_dashboard

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.src.analysis_chain.chain import BaseAnalysisChain

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")

st.set_page_config(layout="wide")

st.title("News Sentiment and Stock Analysis 🧐")

st.markdown(
    """
    This app provides a simple interface to see how the sentiment of news articles about a company has changed over
    the last week, month, or year. Additionally, it retrieves and displays stock price data for the selected company.
"""
)

st.divider()

st.markdown(
    """
    *Note - I have tested the entities in the dropdown box 
    to make sure they present results well. Feel free to enter 
    a different company but don't expect total robustness.*
"""
)

st.divider()

multi_company = st.selectbox(
    label="Select company here", options=["Tesla", "Meta", "JPMorgan"]
)

st.markdown("**Or**")

col1, col2 = st.columns(2)

with col1:
    company = st.text_input(label="Company")
with col2:
    stock_code = st.text_input(label="Stock Ticker (Optional)")

time_frame = st.radio(
    label="How far back would you like to see", options=["One Week", "One Month"]
)

# time_frame = st.select_slider(label = "How far back would you like to see?", options=[str(i) + " Days" for i in range(7, 31)])

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
    st.subheader(
        f"Stock Data for {multi_company if not company else company} ({ticker})"
    )

    if company:
        chain = BaseAnalysisChain(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            company=company,
        )

    else:
        chain = BaseAnalysisChain(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            company=multi_company,
        )

    # run chain
    sentiments_df, total_articles = chain.run()

    try:
        # Retrieve stock price data
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        if not stock_data.empty:
            # Plot the closing prices
            st.write("Closing Prices Over Time:")
        else:
            st.warning("No stock data available for the specified time range.")
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")

    fig = create_dashboard(stock_data, ticker, sentiments_df)
    st.pyplot(fig)
else:
    st.warning("Please provide a valid stock ticker symbol.")
