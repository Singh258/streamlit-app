import streamlit as st
import yfinance as yf
from datetime import datetime

# --- UI Setup ---
st.set_page_config(page_title="Stock Insights", layout="centered")
st.title("📈 Real-Time Stock Insights")

# --- Helper: Format Symbol for Indian Stocks ---
def format_symbol(symbol):
    symbol = symbol.upper().strip()
    if "." not in symbol:  # crude check: assume Indian stock if no suffix
        return symbol + ".NS"
    return symbol

# --- Helper: Convert USD to INR ---
def convert_to_inr(usd_price, rate=83.2):  # Static forex rate, can integrate API later
    return round(usd_price * rate, 2)

# --- User Input ---
symbol_input = st.text_input("🔍 Enter Stock Symbol (e.g., suzlon, TCS, AAPL)")
if symbol_input:
    try:
        formatted_symbol = format_symbol(symbol_input)
        data = yf.Ticker(formatted_symbol)
        hist = data.history(period="1d")

        # --- Metrics Extraction ---
        current_price_usd = round(hist["Close"].iloc[-1], 2)
        day_high_usd = round(hist["High"].iloc[-1], 2)
        day_low_usd = round(hist["Low"].iloc[-1], 2)
        volume = int(hist["Volume"].iloc[-1])

        # --- INR Conversion ---
        price_inr = convert_to_inr(current_price_usd)
        high_inr = convert_to_inr(day_high_usd)
        low_inr = convert_to_inr(day_low_usd)

        # --- Display Core Metrics ---
        st.subheader("📊 Stock Metrics (₹ INR)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Price", f"₹{price_inr}")
        col2.metric("Day High", f"₹{high_inr}")
        col3.metric("Day Low", f"₹{low_inr}")
        col4.metric("Volume", f"{volume:,}")

        # --- Sentiment Stub ---
        sentiment = "Neutral"  # Placeholder
        st.subheader("🧠 Sentiment Analysis")
        if sentiment == "Positive":
            st.success("📈 Positive news sentiment detected — potential buying opportunity.")
        elif sentiment == "Negative":
            st.error("📉 Negative sentiment — caution advised.")
        else:
            st.warning("⚖️ Neutral sentiment — may be worth watching.")

        # --- Advanced Toggle ---
        if st.checkbox("Show Advanced Metrics"):
            atr_inr = round(high_inr - low_inr, 2)
            support = round(low_inr * 0.98, 2)
            resistance = round(high_inr * 1.02, 2)
            st.markdown(f"🌀 Volatility Estimate: **₹{atr_inr}**")
            st.markdown(f"🧱 Support Zone: **₹{support}**, 🚧 Resistance Zone: **₹{resistance}**")

    except Exception as e:
        st.error(f"❌ Data fetch error: {e}")
