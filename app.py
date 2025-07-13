import streamlit as st
import yfinance as yf

# --- UI Setup ---
st.set_page_config(page_title="Stock Insights", layout="centered")
st.title("📈 Real-Time Stock Insights")

# --- Helpers ---
def format_symbol(symbol):
    symbol = symbol.upper().strip()
    if symbol.endswith(".NS"):
        return symbol
    elif "." not in symbol:
        return symbol + ".NS"
    return symbol

def convert_to_inr(usd_price, rate=83.2):
    return round(usd_price * rate, 2)

# --- User Input ---
user_symbol = st.text_input("🔍 Enter Stock Symbol (e.g., RELIANCE, SUZLON, AAPL)")
if user_symbol:
    formatted = format_symbol(user_symbol)
    ticker = yf.Ticker(formatted)
    hist = ticker.history(period="10d")

    if hist.empty or len(hist) < 1:
        st.error("😕 Could not load data for this symbol. Market may be closed or symbol is inactive.")
        st.caption("💡 Try checking the spelling or trying again later.")
    else:
        latest = hist.iloc[-1]
        try:
            current_usd = round(latest["Close"], 2)
            high_usd = round(latest["High"], 2)
            low_usd = round(latest["Low"], 2)
            volume = int(latest["Volume"])

            price_inr = convert_to_inr(current_usd)
            high_inr = convert_to_inr(high_usd)
            low_inr = convert_to_inr(low_usd)

            st.subheader("📊 Stock Metrics (₹ INR)")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Price", f"₹{price_inr}")
            col2.metric("Day High", f"₹{high_inr}")
            col3.metric("Day Low", f"₹{low_inr}")
            col4.metric("Volume", f"{volume:,}")

            st.caption("📅 Showing latest available data from past 10 trading days.")

            # --- Sentiment Stub ---
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
        except Exception as err:
            st.error(f"⚠️ Error parsing data: {err}")

