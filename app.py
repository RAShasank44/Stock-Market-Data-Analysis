import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Stock Market Analysis", layout="wide")
st.title("📈 Stock Market Analysis Dashboard")

# -------------------------------
# Sidebar: User Inputs
# -------------------------------
data_source = st.sidebar.radio("Select Data Source", ["Upload CSV", "Yahoo Finance"])

if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV file to continue.")
        st.stop()
else:
    ticker = st.sidebar.text_input("Enter Stock Ticker", value="TSLA")
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-01-01"))
    @st.cache_data
    def load_data(ticker, start, end):
        data = yf.download(ticker, start=start, end=end)
        data.reset_index(inplace=True)
        return data
    df = load_data(ticker, start_date, end_date)

# -------------------------------
# Check for price column
# -------------------------------
if 'Adj Close' in df.columns:
    price_col = 'Adj Close'
elif 'AdjClose' in df.columns:
    price_col = 'AdjClose'
elif 'Close' in df.columns:
    price_col = 'Close'
else:
    st.error("No price column found in the dataset (Adj Close / AdjClose / Close).")
    st.stop()

# -------------------------------
# Compute Returns & Moving Averages
# -------------------------------
df['Daily_Return'] = df[price_col].pct_change()
df['MA20'] = df[price_col].rolling(20).mean()
df['MA50'] = df[price_col].rolling(50).mean()
df['MA200'] = df[price_col].rolling(200).mean()

# -------------------------------
# Show raw data
# -------------------------------
st.subheader("Raw Data")
st.dataframe(df.head())

# -------------------------------
# Price Chart
# -------------------------------
st.subheader(f"{price_col} Price with Moving Averages")
st.line_chart(df[[price_col, 'MA20', 'MA50', 'MA200']].set_index(df['Date']))

# -------------------------------
# Daily Returns Chart
# -------------------------------
st.subheader("Daily Returns Distribution")
st.bar_chart(df['Daily_Return'].dropna())
