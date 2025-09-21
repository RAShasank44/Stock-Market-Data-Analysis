import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Stock Market Analysis", layout="wide")
st.title("📈 Stock Market Analysis Dashboard")

# Sidebar: User input
ticker = st.sidebar.text_input("Enter Stock Ticker", value="TSLA")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-01-01"))

# Load data
@st.cache_data
def load_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    df.reset_index(inplace=True)
    df['Daily_Return'] = df['Adj Close'].pct_change()
    df['MA20'] = df['Adj Close'].rolling(20).mean()
    df['MA50'] = df['Adj Close'].rolling(50).mean()
    df['MA200'] = df['Adj Close'].rolling(200).mean()
    return df

data = load_data(ticker, start_date, end_date)

st.subheader(f"{ticker} Price Chart")
st.line_chart(data[['Adj Close', 'MA20', 'MA50', 'MA200']].set_index(data['Date']))

st.subheader(f"{ticker} Daily Returns Distribution")
st.bar_chart(data['Daily_Return'].dropna())
