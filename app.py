import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# 🔧 Config
st.set_page_config(page_title="RK Stock Center", layout="centered")
st.title("RK Stock Center 📈")
st.subheader("Live Stock Data + AI News Sentiment")

# 📌 Symbol Input
symbol = st.text_input("Enter stock symbol (e.g. SUZLON.NS, RELIANCE.NS)")

# 📈 Fetch stock data
def fetch_stock_data(symbol):
    try:
        data = yf.download(symbol, period="1mo")
        return data["Close"] if not data.empty else None
    except:
        return None

# 🧠 Fetch news sentiment
def fetch_news_sentiment(symbol):
    try:
        url = f"https://api.marketaux.com/v1/news/all?symbols={symbol}&filter_entities=true&language=en&api_token=YOUR_MARKETAUX_API_KEY"
        res = requests.get(url)
        articles = res.json().get("data", [])
        score = sum(a.get("sentiment_score", 0) for a in articles)
        return score / len(articles) if articles else 0
    except:
        return 0

# 🔍 Process + Display
if symbol:
    st.markdown(f"### {symbol}")
    chart = fetch_stock_data(symbol)
    sentiment = fetch_news_sentiment(symbol)

    if chart is not None:
        st.line_chart(chart)

        if sentiment > 0.3:
            st.success("🟢 Positive sentiment — BUY signal")
        elif sentiment < -0.3:
            st.error("🔴 Negative sentiment — ignore for now")
        else:
            st.info("🟡 Neutral sentiment — monitor")

    else:
        st.warning("⚠️ No data found. Check symbol format or try another.")

    try:
        res = requests.get(url)
        articles = res.json().get("data", [])
        score = sum([a.get("sentiment_score", 0) for a in articles])
        avg = score / len(articles) if articles else 0
        return avg
    except Exception:
        return 0

# 💡 Process
if symbol:
    st.markdown(f"### 📌 {symbol}")
    chart = fetch_stock_data(symbol)
    sentiment = fetch_news_sentiment(symbol)

    if chart is not None and not chart.empty:
        st.line_chart(chart)

        if sentiment > 0.3:
            st.success("🟢 Positive news sentiment — relevant for BUY consideration.")
        elif sentiment < -0.3:
            st.error("🔴 Negative sentiment — not relevant currently.")
        else:
            st.info("🟡 Neutral sentiment — monitor further.")
    else:
        st.warning("⚠️ No stock data found. Please check symbol or API limits.")

