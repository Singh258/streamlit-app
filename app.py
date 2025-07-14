import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Indian Stock Tracker", layout="centered")
st.title("📊 Real-Time NSE Stock Price (INR)")

symbol = st.text_input("Enter NSE stock symbol (e.g., SUZLON)", value="SUZLON").strip().upper()
ticker = f"{symbol}.NS"

if symbol:
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get("currentPrice")
        hist = stock.history(period="5d", interval="1h")

        if price is None or hist.empty:
            st.error("❌ No data found. Try a valid NSE symbol like TATAMOTORS or RELIANCE.")
        else:
            st.metric("Current Price (INR)", f"₹{price}")
            st.line_chart(hist["Close"])
            st.success("✅ Data fetched successfully.")
    except Exception as e:
        st.error(f"❌ Error: {e}")



