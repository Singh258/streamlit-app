import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# 🔧 Page config
st.set_page_config(page_title="RK Stock Center", layout="centered")
st.title("RK Stock Center 📈")
st.subheader("Live Stock Screener with AI-Powered News Sentiment")

# 📌 Symbol input field
symbol = st.text_input("Enter stock symbol (e.g. SUZLON.NS, RELIANCE.NS, TCS.NS)")

# 📈 Function to fetch stock data
def fetch_stock_data(symbol):
    try:
        data = yf.download(symbol, period="1mo")
        if data.empty:
            return None
        return data["Close"]
    except Exception:
        return None

# 🧠 Function to fetch news sentiment
def fetch_news_sentiment(symbol):
    try:
        url = f"https://api.marketaux.com/v1/news/all?symbols={symbol}&filter_entities=true&language=en&api_token=YOUR_MARKETAUX_API_KEY"
        response = requests.get(url)
        articles = response.json().get("data", [])
        sentiment_score = sum(article.get("sentiment_score", 0) for article in articles)
        avg_sentiment = sentiment_score / len(articles) if articles else 0
        return avg_sentiment
    except Exception:
        return 0

# 🔍 Processing section
if symbol:
    st.markdown(f"### Stock: {symbol}")
    chart_data = fetch_stock_data(symbol)
    news_sentiment = fetch_news_sentiment(symbol)

    if chart_data is not None:
        st.line_chart(chart_data)

        # 💡 Sentiment suggestion
        if news_sentiment > 0.3:
            st.success("🟢 Positive sentiment — BUY signal")
        elif news_sentiment < -0.3:
            st.error("🔴 Negative sentiment — avoid for now")
        else:
            st.info("🟡 Neutral sentiment — watchlist candidate")
    else:
        st.warning("⚠️ No stock data found. Check symbol format or try another.")

