import streamlit as st
import pandas as pd
import yfinance as yf
from difflib import get_close_matches

# List of known Indian stock symbols (extendable)
known_symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "HDFC", "ITC", "WIPRO", "LT", "ADANIENT", "ADANIPORTS", "YESBANK", "IRFC", "IDEA", "SUZLON", "JPPOWER"]

# Suggest closest match for incorrect typing
def suggest_symbol(user_input):
    matches = get_close_matches(user_input.upper(), known_symbols, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Page setup
st.set_page_config(page_title="Ritesh Stock Tracker", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 Ritesh Stock Tracker (AI-Enhanced)</h1>", unsafe_allow_html=True)

# Glassmorphism CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: rgba(255, 255, 255, 0.15);
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

# Stock symbol input
st.subheader("🔍 Search Any Stock (No need to add .NS)")
user_input = st.text_input("Enter stock name (e.g. RELIANCE, TCS)")

# Autocorrect + .NS auto handling
if user_input:
    user_input = user_input.upper().strip()
    if user_input not in known_symbols:
        suggestion = suggest_symbol(user_input)
        if suggestion:
            st.info(f"Did you mean **{suggestion}**? Showing data for it.")
            user_input = suggestion
        else:
            st.warning("Couldn't recognize this stock. Please check spelling.")

    # Append .NS for Indian stocks
    full_symbol = f"{user_input}.NS"

    # Fetch live price
    try:
        stock = yf.Ticker(full_symbol)
        data = stock.history(period="1d", interval="1m")
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            st.success(f"💰 Current Price of {user_input}: ₹{round(current_price, 2)}")
        else:
            st.warning("⚠️ No data available right now.")
    except Exception as e:
        st.error(f"Error fetching stock: {e}")

# Penny Stocks section (static demo)
st.subheader("💹 Penny Stocks (Price < ₹50) - Demo")
demo_penny = pd.DataFrame({
    "Symbol": ["IRFC", "YESBANK", "IDEA", "SUZLON", "JPPOWER"],
    "Price (₹)": [46.0, 24.5, 13.2, 38.0, 18.5]
})
st.table(demo_penny)

# Footer
st.markdown("<hr><center>©2023 Ritesh Stock Tracker</center>", unsafe_allow_html=True)
