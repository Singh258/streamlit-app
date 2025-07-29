import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="NSE Tracker", layout="centered")
st.markdown("<h1 style='text-align: center;'>📈 Live NSE Stock Tracker</h1>", unsafe_allow_html=True)

# 🔁 Cache the symbol list for performance
@st.cache_data
def fetch_symbol_list():
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"  # Replace with NSE list if available
    df = pd.read_csv(url)
    return sorted(df['Name'].tolist())[:200]  # Limit to top 200 to prevent overload

symbols = fetch_symbol_list()
selected = st.selectbox("🔍 Select a Stock", symbols)

# 📊 Fetch live price
def get_live_price(symbol):
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            return None
        return round(data['Close'].iloc[-1], 2)
    except Exception as e:
        return None

if selected:
    price = get_live_price(selected)
    if price:
        st.success(f"💰 Live Price of {selected}: ₹{price}")
    else:
        st.error("⚠️ No data found or failed to fetch.")
st.dataframe(demo_df)

# Footer
st.markdown("<hr><center>©2023 Ritesh Stock Tracker</center>", unsafe_allow_html=True)
