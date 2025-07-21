import streamlit as st
import yfinance as yf

# 🔰 Page config for branding
st.set_page_config(
    page_title="Ritesh Stock Real Time Tracker",
    page_icon="📈",
    layout="centered"
)

# 🔰 App header
st.title("📊 Ritesh Stock Real Time Tracker")
st.markdown("Track live stock prices with zero static fallback. Built for precision. 🔧")

# 🔰 Ticker input
ticker = st.text_input("Enter Stock Ticker (e.g. RELIANCE.NS)", value="RELIANCE.NS")

if ticker:
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")

        if not data.empty:
            latest_price = data["Close"].iloc[-1]
            st.metric(label="📈 Latest Price", value=f"₹{latest_price:.2f}")
            st.line_chart(data["Close"])
        else:
            st.error("❌ No live data available. Check ticker or try again in a few minutes.")
    except Exception as e:
        st.error(f"⚠️ Error fetching data: {str(e)}")
