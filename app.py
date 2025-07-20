import streamlit as st
import yfinance as yf
from difflib import get_close_matches

st.set_page_config(page_title="Ritesh Stock Tracker", layout="centered")

@st.cache_data
def load_symbols():
    return [
        "RELIANCE", "SUZLON", "INFY", "TATAMOTORS", "SBIN", "ICICIBANK",
        "HDFC", "ONGC", "ITC", "MARUTI", "LT", "IDFC", "YESBANK", "BANKBARODA"
    ]

def resolve_symbol(name):
    name = name.strip().upper().replace(".NS", "")
    symbols = load_symbols()
    if name in symbols:
        return name + ".NS"
    match = get_close_matches(name, symbols, n=1, cutoff=0.4)
    if match:
        return match[0] + ".NS"
    return None

def get_data(sym):
    try:
        ticker = yf.Ticker(sym)
        hist = ticker.history(period="1d", interval="1m")
        latest = hist.tail(1)
        if latest.empty:
            return None
        return {
            "price": round(latest["Close"].iloc[0], 2),
            "high": round(latest["High"].iloc[0], 2),
            "low": round(latest["Low"].iloc[0], 2),
            "open": round(latest["Open"].iloc[0], 2),
            "volume": int(latest["Volume"].iloc[0])
        }
    except:
        return None

st.markdown("<h2 style='text-align:center;'>📈 Ritesh Stock Price App</h2>", unsafe_allow_html=True)

query = st.text_input("Enter stock name or symbol")
resolved = resolve_symbol(query)

if resolved:
    data = get_data(resolved)
    if data:
        st.success(f"Symbol: {resolved}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Price ₹", data["price"])
        col2.metric("High ₹", data["high"])
        col3.metric("Low ₹", data["low"])
        col4, col5 = st.columns(2)
        col4.metric("Open ₹", data["open"])
        col5.metric("Volume", f"{data['volume']:,}")
    else:
        st.warning("⚠️ Data not available. Try again shortly.")
elif query:
    st.error("❌ Symbol not recognized. Please check spelling.")


