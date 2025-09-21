import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📈 Stock Market Analysis - Flexible Date Option")

# -------------------------------
# Upload CSV
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file is None:
    st.warning("Please upload a CSV file with at least 'Close' column.")
    st.stop()

df = pd.read_csv(uploaded_file)
st.write("Columns detected:", df.columns.tolist())

# -------------------------------
# User selects mode
# -------------------------------
mode = st.radio("Select Mode:", ["With Date", "Without Date"])

# -------------------------------
# Columns check
# -------------------------------
price_col = st.selectbox("Select Price Column:", df.columns.tolist(), index=df.columns.get_loc('Close') if 'Close' in df.columns else 0)

if price_col not in df.columns:
    st.error(f"CSV must have a '{price_col}' column.")
    st.stop()

# -------------------------------
# With Date Mode
# -------------------------------
if mode == "With Date":
    date_col_candidates = ['Date', 'date', 'Timestamp', 'timestamp']
    date_col = None
    for col in date_col_candidates:
        if col in df.columns:
            date_col = col
            break
    if date_col is None:
        st.error("No date column found. Either upload a CSV with a date column or select 'Without Date' mode.")
        st.stop()

    df[date_col] = pd.to_datetime(df[date_col])
    df.set_index(date_col, inplace=True)

# -------------------------------
# Without Date Mode - create synthetic dates
# -------------------------------
else:
    df['Date'] = pd.date_range(start='2020-01-01', periods=len(df), freq='D')
    df.set_index('Date', inplace=True)

# -------------------------------
# Compute Moving Averages
# -------------------------------
df['MA20'] = df[price_col].rolling(20).mean()
df['MA50'] = df[price_col].rolling(50).mean()
df['MA200'] = df[price_col].rolling(200).mean()
df['Daily_Return'] = df[price_col].pct_change()

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

# -------------------------------
# Summary Statistics
# -------------------------------
st.subheader("Summary Statistics")
st.write(df.describe())
