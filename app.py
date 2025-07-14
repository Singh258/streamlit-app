import streamlit as st
import yfinance as yf

# Page setup
st.set_page_config(page_title="📈 Ritesh Real Time Stock Tracker", layout="centered")
st.title("📊 Ritesh Real Time NSE Stock Tracker")

st.markdown("Track live NSE stock data in INR. Enter a symbol OR explore penny stocks under ₹100 🪙")

# --- User Input Section ---
symbol = st.text_input("🔎 Enter NSE stock symbol (e.g., SUZLON, INFY, RELIANCE)").strip().upper()

search = st.button("📥 Search Price")

# --- Symbol-Based Price Fetch ---
if symbol and search:
    ticker = f"{symbol}.NS"
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get("currentPrice")
        hist = stock.history(period="5d", interval="1h")

        if price is None and hist.empty:
            st.error("❌ No data found. Invalid symbol or rate limit reached.")
        elif price is None:
            st.warning("⚠️ Price unavailable. Try again later.")
        elif hist.empty:
            st.warning("⚠️ Chart data unavailable. API may be throttled.")
        else:
            st.metric("Current Price (INR)", f"₹{price}")
            st.line_chart(hist["Close"])
            st.success(f"✅ Data fetched for {symbol}")
    except Exception as e:
        st.error(f"🚨 Error: {e}")

# --- Penny Stock List Button ---
show_penny = st.button("📉 Show Stocks Below ₹100")

if show_penny:
    st.subheader("💡 Stocks Under ₹100 (Sample List)")

    penny_stocks = {
        "SUZLON.NS": "Suzlon Energy",
        "IRFC.NS": "Indian Railway Finance",
        "YESBANK.NS": "Yes Bank",
        "IDEA.NS": "Vodafone Idea",
        "NHPC.NS": "NHPC Ltd",
        "BANKINDIA.NS": "Bank of India",
        "UNIONBANK.NS": "Union Bank"
    }

    for ticker, name in penny_stocks.items():
        try:
            data = yf.Ticker(ticker).info
            price = data.get("currentPrice")
            if price and price < 100:
                st.write(f"📌 **{name}** (`{ticker}`): ₹{price}")
        except:
            st.write(f"⚠️ Could not fetch price for {name} ({ticker})")



