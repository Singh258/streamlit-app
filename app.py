import streamlit as st
import yfinance as yf

# --- UI Setup ---
st.set_page_config(page_title="Stock Insights", layout="centered")
st.title("📈 Real-Time Stock Insights")

# --- Helper Functions ---
def format_symbol(symbol):
    symbol = symbol.upper().strip()
    if "." not in symbol:
        return symbol + ".NS"
    return symbol

def convert_to_inr(usd_price, rate=83.2):
    return round(usd_price * rate, 2)

# --- User Input ---
symbol_input = st.text_input("🔍 Enter Stock Symbol (e.g., suzlon, TCS, AAPL)")
if symbol_input:
    formatted_symbol = format_symbol(symbol_input)
    data = yf.Ticker(formatted_symbol)
    hist = data.history(period="10d")

    if hist.empty or len(hist) < 1:
        st.error("😕 Data not loaded. Market may be closed or symbol inactive.")
    else:
        latest = hist.iloc[-1]
        current_price_usd = round(latest["Close"], 2)
        day_high_usd = round(latest["High"], 2)
        day_low_usd = round(latest["Low"], 2)
        volume = int(latest["Volume"])

        price_inr = convert_to_inr(current_price_usd)
        high_inr = convert_to_inr(day_high_usd)
        low_inr = convert_to_inr(day_low_usd)

        st.subheader("📊 Stock Metrics (₹ INR)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Price", f"₹{price_inr}")
        col2.metric("Day High", f"₹{high_inr}")
        col3.metric("Day Low", f"₹{low_inr}")
        col4.metric("Volume", f"{volume:,}")

        st.caption("📅 Latest available data fetched from last 10 trading days")

        # --- Sentiment Placeholder ---
        st.subheader("🧠 Sentiment Analysis")
        sentiment = "Neutral"
        if sentiment == "Positive":
            st.success("📈 Positive sentiment detected — potential buying opportunity.")
        elif sentiment == "Negative":
            st.error("📉 Negative sentiment — caution advised.")
        else:
            st.warning("⚖️ Neutral sentiment — may be worth watching.")

        # --- Optional Advanced Metrics ---
        if st.checkbox("Show Advanced Metrics"):
            atr_inr = round(high_inr - low_inr, 2)
            support = round(low_inr * 0.98, 2)
            resistance = round(high_inr * 1.02, 2)
            st.markdown(f"🌀 Volatility Estimate: **₹{atr_inr}**")
            st.markdown(f"🧱 Support Zone: **₹{support}**, 🚧 Resistance Zone: **₹{resistance}**")
