import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# App title
st.set_page_config(page_title="StockLens", layout="centered")
st.markdown("<h1 style='text-align: center;'>📈 StockLens</h1>", unsafe_allow_html=True)

# Glassmorphism CSS style
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
        margin-top: 20px;
        color: white;
    }
    .reportview-container .markdown-text-container {
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Stock search
st.subheader("🔍 Search Stock Live Price")
stock_symbol = st.text_input("Enter Stock Symbol (e.g., TCS.NS for NSE, AAPL for US)")

if stock_symbol:
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="1d", interval="1m")
        current_price = data['Close'].iloc[-1]
        st.success(f"💰 Current Price of {stock_symbol.upper()}: ₹{round(current_price, 2)}")
    except Exception as e:
        st.error(f"Error fetching data: {e}")

# Penny stock section
st.subheader("💹 Penny Stocks (Below ₹50)")

def get_nse_penny_stocks():
    try:
        url = "https://www.niftytrader.in/stock-analysis"
        df_list = pd.read_html(url)
        df = df_list[0]
        df.columns = [col.strip() for col in df.columns]
        penny_df = df[df['Price'] < 50].sort_values(by="Price")
        return penny_df[['Symbol', 'Price', 'Change %']].head(10)
    except:
        return pd.DataFrame(columns=["Symbol", "Price", "Change %"])

penny_stocks = get_nse_penny_stocks()

if not penny_stocks.empty:
    st.table(penny_stocks)
else:
    st.info("Could not load penny stock data currently.")

# Footer
st.markdown("<hr><center>©2023 StockLens</center>", unsafe_allow_html=True)

