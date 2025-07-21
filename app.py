import streamlit as st
import pandas as pd
import yfinance as yf
from difflib import get_close_matches

# Version tag to confirm deploy
st.caption("🧪 Debug Mode: v2.1")

# Known Indian stock symbols
known_symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "HDFC", "ITC", "WIPRO", "LT", "ADANIENT", "ADANIPORTS", "YESBANK", "IRFC", "IDEA", "SUZLON", "JPPOWER"]

def suggest_symbol(user_input):
    matches = get_close_matches(user_input.upper(), known_symbols, n=1, cutoff=0.6)
    return matches[0] if matches else None

# App Title
st.set_page_config(page_title="Ritesh Stock Tracker", layout="centered")
st.markdown("<h1 style='text-align: center;'>📊 Ritesh Stock Tracker (Debug)</h1>", unsafe_allow_html=True)

# Input Field
st.subheader("🔍 Search Any Stock (no need to add .NS)")
user_input = st.text_input("Enter stock name:")

if user_input:
    user_input = user_input.upper().strip()
    if user_input not in known_symbols:
        suggestion = suggest_symbol(user_input)
        if suggestion:
            st.info(f"Did you mean **{suggestion}**? Showing data for it.")
            user_input = suggestion
        else:
            st.warning("Symbol not found in known list. Defaulting to RELIANCE")
            user_input = "RELIANCE"
    try:
        full_symbol = f"{user_input}.NS"
        stock = yf.Ticker(full_symbol)
        data = stock.history(period="1d", interval="1m")

        if not data.empty:
            current_price = data['Close'].iloc[-1]
            st.success(f"💰 Live Price of {user_input}: ₹{round(current_price, 2)}")
        else:
            st.warning("⚠️ No data returned from Yahoo Finance.")
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")

# Demo Penny Stocks Table
st.subheader("💹 Penny Stocks Demo (Static Data)")
demo_df = pd.DataFrame({
    "Symbol": ["IRFC", "YESBANK", "IDEA", "SUZLON", "JPPOWER"],
    "Price (₹)": [46.0, 24.5, 13.2, 38.0, 18.5]
})
st.dataframe(demo_df)

# Footer
st.markdown("<hr><center>©2023 Ritesh Stock Tracker</center>", unsafe_allow_html=True)
