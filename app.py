import streamlit as st
import yfinance as yf
from difflib import get_close_matches

st.set_page_config(page_title="Ritesh Stock Tracker", layout="centered")

@st.cache_data
def load_symbols():
    return [
        "RELIANCE", "SUZLON", "INFY", "TATAMOTORS", "SBIN", "ICICIBANK",
        "HDFC", "ONGC", "ITC", "MARUTI", "LT", "IDFC", "YESBANK"
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
        fast = ticker.fast_info
        return {
            "price": round(fast.get("last_price", 0), 2),
            "high": round(fast.get("day_high", 0), 2),
            "low": round(fast.get("day_low", 0), 2),
            "open": round(fast.get("open", 0), 2),
            "prev": round(fast.get("previous_close", 0), 2),
            "volume": fast.get("last_volume", 0)
        }
    except:
        return None

st.markdown("<h2 style='text-align:center;'>🔍 Ritesh Stock Price App</h2>", unsafe_allow_html=True)
query = st.text_input("Enter stock name or symbol")
resolved = resolve_symbol(query)

if resolved:
    data = get_data(resolved)
    if data and data["price"] > 0:
        st.success(f"Symbol: {resolved}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Price ₹", data["price"])
        col2.metric("High ₹", data["high"])
        col3.metric("Low ₹", data["low"])
        col4, col5, col6 = st.columns(3)
        col4.metric("Open ₹", data["open"])
        col5.metric("Prev Close ₹", data["prev"])
        col6.metric("Volume", f"{data['volume']:,}")
    else:
        st.warning("⚠️ Data not available.")
elif query:
    st.error("❌ Symbol not recognized.")


