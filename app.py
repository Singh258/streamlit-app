import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# App config and title
st.set_page_config(page_title="Ritesh Real Stock Tracker", layout="centered")
st.markdown("<h1 style='text-align: center;'>📊 Ritesh Real Stock Tracker</h1>", unsafe_allow_html=True)

# Glassmorphism CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 2rem;
        color: white;
    }
    .reportview-container .markdown-text-container {
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Search bar
st.subheader("🔍 Search Live Stock Price")
stock_symbol = st.text_input("Enter Stock Symbol (e.g. RELIANCE.NS, INFY.NS)")

if stock_symbol:
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="1d", interval="1m")
        current_price = data['Close'].iloc[-1]
        st.success(f"💰 Current Price of {stock_symbol.upper()}: ₹{round(current_price, 2)}")
    except Exception as e:
        st.error("⚠️ Unable to fetch stock price. Please check symbol or try again later.")

# Penny Stock Section
st.subheader("💹 Penny Stocks (Price < ₹50)")

def get_penny_stocks():
    try:
        url = "https://www.moneycontrol.com/stocks/marketstats/nse-loser/all-companies_0_0/index.html"
        df_list = pd.read_html(url)
        df = df_list[0]
        df.columns = [col.strip() for col in df.columns]
        df = df.rename(columns={"Company Name": "Symbol", "Last Price": "Price"})
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        penny_df = df[df['Price'] < 50].sort_values("Price").dropna()
        return penny_df[['Symbol', 'Price']].head(10)
    except:
        return pd.DataFrame(columns=["Symbol", "Price"])

penny_stocks = get_penny_stocks()

if not penny_stocks.empty:
    st.table(penny_stocks)
else:
    st.info("📡 Unable to load penny stocks currently. Please try again later.")

# Footer
st.markdown("<hr><center>©2023 Ritesh Real Stock Tracker</center>", unsafe_allow_html=True)


