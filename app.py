import streamlit as st
import yfinance as yf

# App layout
st.set_page_config(page_title="📈 Indian Stock Tracker", layout="centered")
st.title("📊 Real-Time NSE Stock Price (INR)")

# User input
symbol = st.text_input("Enter NSE stock symbol (e.g., SUZLON)", value="SUZLON").strip().upper()
ticker = f"{symbol}.NS"

if symbol:
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get("currentPrice")
        hist = stock.history(period="5d", interval="1h")

        # Combined Data Check
        if price is None and hist.empty:
            st.error("❌ No data returned. Either symbol is invalid or rate limit has been hit.")
        elif price is None:
            st.warning("⚠️ Price unavailable. Retry later or verify symbol.")
        elif hist.empty:
            st.warning("⚠️ Chart data not available. Might be API cooldown or symbol issue.")
        else:
            st.metric("Current Price (INR)", f"₹{price}")
            st.line_chart(hist["Close"])
            st.success("✅ Stock data fetched successfully.")
    except Exception as e:
        st.error(f"🚨 Internal error: {e}")



