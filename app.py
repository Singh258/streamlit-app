# --------------------------------------------
# 📈 StockApp — Clean, Reliable NSE Tracker
# --------------------------------------------

import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="📈 StockApp — Live Tracker", layout="wide")
st.markdown("<h1 style='text-align:center;'>📊 StockApp — Live Price & Penny Screener</h1>", unsafe_allow_html=True)

def normalize(symbol):
    if not symbol: return None
    s = symbol.strip().upper()
    return s if s.endswith(".NS") else f"{s}.NS"

def fetch(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1d", interval="5m").tail(1)
        if not data.empty:
            return {
                "symbol": symbol,
                "price": round(data["Close"].iloc[0], 2),
                "high": round(data["High"].iloc[0], 2),
                "low": round(data["Low"].iloc[0], 2),
                "open": round(data["Open"].iloc[0], 2),
                "volume": int(data["Volume"].iloc[0]),
                "time": datetime.now().strftime('%H:%M:%S')
            }
    except: return None
    return None

@st.cache_data(ttl=1800)
def scan_penny(stocks):
    out = []
    for s in stocks:
        d = fetch(s)
        if d and 1 < d["price"] < 50:
            out.append({
                "Symbol": s,
                "Price ₹": d["price"],
                "High ₹": d["high"],
                "Low ₹": d["low"],
                "Volume": d["volume"],
                "Time": d["time"]
            })
    return pd.DataFrame(out)

def error_msg(s):
    st.error(f"❌ No data for `{s}`.")
    st.caption("Retry later or check symbol.")

watchlist = [
    "SUZLON.NS", "JPPOWER.NS", "IDEA.NS", "IRFC.NS", "NHPC.NS", "SJVN.NS", "IDFC.NS",
    "YESBANK.NS", "IOB.NS", "UNIONBANK.NS", "BANKBARODA.NS", "NBCC.NS", "GMRINFRA.NS",
    "PFC.NS", "BHEL.NS", "HUDCO.NS", "RVNL.NS", "UCOBANK.NS", "CENTRALBK.NS", "LICI.NS"
]

tab1, tab2, tab3 = st.tabs(["🔍 Price Lookup", "💸 Penny Screener", "📘 Help"])

with tab1:
    q = st.text_input("Enter NSE symbol (e.g. RELIANCE, TCS)")
    if q:
        s = normalize(q)
        d = fetch(s)
        if d:
            st.success(f"✅ {s} — {d['time']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Price ₹", d["price"])
            c2.metric("High ₹", d["high"])
            c3.metric("Low ₹", d["low"])
            c4, c5 = st.columns(2)
            c4.metric("Open ₹", d["open"])
            c5.metric("Volume", f"{d['volume']:,}")
        else:
            error_msg(s)

with tab2:
    st.info("Scanning stocks under ₹50...")
    df = scan_penny(watchlist)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ No penny stock data available now.")

with tab3:
    st.markdown("""
    ### 📘 Help
    - Type any valid NSE symbol like `TCS`, `RELIANCE`, etc.
    - Penny tab lists real-time prices under ₹50.
    - App uses free `yfinance` API — no storage or signup.
    - Default fetch is 5-minute interval — most stable.
    """)
