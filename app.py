import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Stock Market Analysis", layout="wide")
st.title("📈 Stock Market Analysis Dashboard")

# -------------------------------
# Sidebar: Select Data Source
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
        # Flatten MultiIndex if present
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = ['_'.join([str(c) for c in col]).strip() for col in data.columns.values]
        return data

    df = load_data(ticker, start_date, end_date)

# -------------------------------
# Detect price column
# -------------------------------
price_candidates = ['Adj Close']
price_col = None
for col in price_candidates:
    if col in df.columns:
        price_col = col
        break

if price_col is None:
    st.error("No price column found. Make sure your CSV has 'Close' or 'Adj Close'.")
    st.stop()

# -------------------------------
# Detect date column
# -------------------------------
date_candidates = ['Date', 'date', 'DATE']
date_col = None
for col in date_candidates:
    if col in df.columns:
        date_col = col
        break

if date_col is None:
    st.error("No date column found in dataset.")
    st.stop()

# -------------------------------
# Prepare DataFrame
# -------------------------------
df[date_col] = pd.to_datetime(df[date_col])
df.set_index(date_col, inplace=True)

# -------------------------------
# Compute Daily Returns & Moving Averages
# -------------------------------
df['Daily_Return'] = df[price_col].pct_change()
df['MA20'] = df[price_col].rolling(20).mean()
df['MA50'] = df[price_col].rolling(50).mean()
df['MA200'] = df[price_col].rolling(200).mean()

# -------------------------------
# Display Raw Data
# -------------------------------
st.subheader("Raw Data Preview")
st.dataframe(df.head())

# -------------------------------
# Price with Moving Averages
# -------------------------------
st.subheader(f"{price_col} Price with Moving Averages")
st.line_chart(df[[price_col, 'MA20', 'MA50', 'MA200']])

# -------------------------------
# Daily Returns Chart
# -------------------------------
st.subheader("Daily Returns Distribution")
st.bar_chart(df['Daily_Return'].dropna())
