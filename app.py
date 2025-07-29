import streamlit as st
import pandas as pd
import yfinance as yf

# 🌐 Page config
st.set_page_config(page_title="📈 Live NSE Stock Tracker", layout="centered")
st.markdown("<h1 style='text-align: center;'>📈 Live NSE Stock Tracker</h1>", unsafe_allow_html=True)

# 🗂 Cached NSE symbol list
@st.cache_data
def fetch_symbol_list():
    url = "https://raw.githubusercontent.com/AnkurMourya/NSE-Stock-List/main/NSE_stock_list.csv"
    df = pd.read_csv(url)
    return sorted(df['SYMBOL'].dropna().unique().tolist())[:200]  # Safety cap for performance

symbols = fetch_symbol_list()
selected = st.selectbox("🔍 Select NSE Stock", symbols)

# 💹 Live price fetch with error handling
def get_live_price(symbol):
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        data = ticker.history(period="1d", interval="1m")
        return round(data['Close'].iloc[-1], 2) if not data.empty else None
    except Exception:
        return None

# 🔔 Output
if selected:
    price = get_live_price(selected)
    if price:
        st.success(f"💰 Live Price of {selected}: ₹{price}")
    else:
        st.error("⚠️ No data found or failed to fetch.")
