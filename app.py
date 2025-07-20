import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="📈 NSE Tracker", layout="wide")
st.markdown("<h1 style='text-align:center;'>📊 NSE Stock Viewer & Penny Screener</h1>", unsafe_allow_html=True)

def normalize(symbol):
    if not symbol: return None
    symbol = symbol.strip().upper()
    return symbol + ".NS" if not symbol.endswith(".NS") else symbol

def fetch(symbol, retries=3, delay=2):
    for i in range(retries):
        try:
            t = yf.Ticker(symbol)
            h = t.history(period="1d", interval="1m").tail(1)
            if not h.empty:
                return {
                    "symbol": symbol,
                    "price": round(h["Close"].iloc[0], 2),
                    "high": round(h["High"].iloc[0], 2),
                    "low": round(h["Low"].iloc[0], 2),
                    "open": round(h["Open"].iloc[0], 2),
                    "volume": int(h["Volume"].iloc[0]),
                    "time": datetime.now().strftime('%H:%M:%S')
                }
        except: pass
        time.sleep(delay * (i + 1))
    return None

@st.cache_data(ttl=1800)
def scan_penny(symbols, threshold=50):
    result = []
    for s in symbols:
        d = fetch(s)
        if d and 1 < d["price"] < threshold:
            result.append({
                "Symbol": s,
                "Price ₹": d["price"],
                "High ₹": d["high"],
                "Low ₹": d["low"],
                "Volume": d["volume"],
                "Time": d["time"]
            })
    return pd.DataFrame(result)

def error(symbol):
    st.error(f"❌ No data found for `{symbol}`.")
    st.caption("Check symbol or retry later.")

symbol_list = [
    "SUZLON.NS", "JPPOWER.NS", "IDEA.NS", "IRFC.NS", "NHPC.NS", "SJVN.NS",
    "IDFC.NS", "YESBANK.NS", "IOB.NS", "UNIONBANK.NS", "BANKBARODA.NS",
    "NBCC.NS", "GMRINFRA.NS", "PFC.NS", "BHEL.NS", "HUDCO.NS", "LICI.NS",
    "RVNL.NS", "UCOBANK.NS", "CENTRALBK.NS", "MAHABANK.NS", "COALINDIA.NS"
]

tab1, tab2, tab3 = st.tabs(["🔍 Stock", "💸 Penny Stocks", "📘 Help"])

with tab1:
    query = st.text_input("Enter NSE symbol (e.g. RELIANCE, TCS, BANKBARODA)")
    if query:
        s = normalize(query)
        d = fetch(s)
        if d:
            st.success(f"✅ {s} — {d['time']}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Price ₹", d["price"])
            col2.metric("High ₹", d["high"])
            col3.metric("Low ₹", d["low"])
            col4, col5 = st.columns(2)
            col4.metric("Open ₹", d["open"])
            col5.metric("Volume", f"{d['volume']:,}")
        else:
            error(s)

with tab2:
    st.info("Scanning penny stocks below ₹50...")
    df = scan_penny(symbol_list)
    if not df.empty:
        st.subheader("📋 Penny Stocks Live")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Penny data unavailable. Retry later.")

with tab3:
    st.markdown("""
    ### 📘 Help Guide
    - Enter valid NSE symbols like `TCS`, `RELIANCE`, `SUZLON`, etc.
    - Penny tab shows live prices for low-cap stocks under ₹50.
    - Uses free yfinance API with retry logic.
    - No data stored — all fetched live.
    """)
