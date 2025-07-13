import streamlit as st
import yfinance as yf
from datetime import datetime

# --- UI Setup ---
st.set_page_config(page_title="Stock Insights", layout="centered")
st.title("📈 Real-Time Stock Insights")

# --- User Input ---
symbol = st.text_input("🔍 Enter Stock Symbol (e.g., AAPL, TCS.NS)")
if symbol:
    try:
        # --- Data Fetching ---
        data = yf.Ticker(symbol)
        hist = data.history(period="1d")
        
        # --- Metrics Extraction ---
        current_price = round(hist["Close"].iloc[-1], 2)
        day_high = round(hist["High"].iloc[-1], 2)
        day_low = round(hist["Low"].iloc[-1], 2)
        volume = int(hist["Volume"].iloc[-1])

        # --- Display Core Metrics ---
        st.subheader("📊 Stock Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Price", f"${current_price}")
        col2.metric("Day High", f"${day_high}")
        col3.metric("Day Low", f"${day_low}")
        col4.metric("Volume", f"{volume:,}")

        # --- Sentiment Stub ---
        sentiment = "Neutral"  # Placeholder until NLP or news API added
        st.subheader("🧠 Sentiment Analysis")
        if sentiment == "Positive":
            st.success("📈 Positive news sentiment detected — potential buying opportunity.")
        elif sentiment == "Negative":
            st.error("📉 Negative sentiment — caution advised.")
        else:
            st.warning("⚖️ Neutral sentiment — may be worth watching.")

        # --- Advanced Toggle ---
        if st.checkbox("Show Advanced Metrics"):
            atr = round(day_high - day_low, 2)
            support = round(day_low * 0.98, 2)
            resistance = round(day_high * 1.02, 2)
            st.markdown(f"🌀 Volatility Estimate (ATR-like): **{atr}**")
            st.markdown(f"🧱 Support Zone: **{support}**, 🚧 Resistance Zone: **{resistance}**")

    except Exception as e:
        st.error(f"❌ Data fetch error: {e}")

