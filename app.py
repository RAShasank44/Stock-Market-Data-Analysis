import streamlit as st
import pandas as pd

st.title("Stock Dashboard")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Columns in CSV:", df.columns.tolist())
    
    # Use 'Close' column explicitly
    if 'Close' not in df.columns:
        st.error("CSV must have a 'Close' column.")
        st.stop()

    # Use 'Date' column
    if 'Date' not in df.columns:
        st.error("CSV must have a 'Date' column.")
        st.stop()

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()
    
    st.subheader("Price with Moving Averages")
    st.line_chart(df[['Close','MA20','MA50']])
