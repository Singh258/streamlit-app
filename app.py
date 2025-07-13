import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# 🔧 CONFIG
st.set_page_config(page_title="RK Stock Center", layout="centered")
st.title("RK Stock Center 📈")
st.subheader("Live Penny Stock Screener with AI News Analysis")

# 📅 Date Range
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

# 🔑 API Keys (replace with your actual keys)
ALPHA_VANTAGE_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
MARKETAUX_KEY = "YOUR_MARKETAUX_API_KEY"

# 📥 Penny Stock Symbols (example list — can be expanded)
penny_symbols = ["IDEA.BSE", "JPPOWER.BSE", "SUZLON.BSE", "YESBANK.BSE"]

# 📊 Function to fetch stock data
def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        prices = data.get("Time Series (Daily)", {})
        df = pd.DataFrame.from_dict(prices, orient="index")
        df = df.rename(columns={"4. close": "Close"})
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df = df.sort_index().tail(30)
        return df["Close"]
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

# 🧠 Function to fetch news sentiment
def fetch_news_sentiment(symbol):
    url = f"https://api.marketaux.com/v1/news/all?symbols={symbol}&filter_entities=true&language=en&api_token={MARKETAUX_KEY}"
    try:
        response = requests.get(url)
        news_data = response.json()
        articles = news_data.get("data", [])
        sentiment_score = 0
        for article in articles:
            sentiment = article.get("sentiment_score", 0)
            sentiment_score += sentiment
        avg_sentiment = sentiment_score / len(articles) if articles else 0
        return avg_sentiment
    except Exception as e:
        st.error(f"Error fetching news for {symbol}: {e}")
        return 0

# 🔍 Display Results
for symbol in penny_symbols:
    st.markdown(f"### 📌 {symbol}")
    chart = fetch_stock_data(symbol)
    sentiment = fetch_news_sentiment(symbol)

    if chart is not None:
        st.line_chart(chart)

        # 🧠 AI-style suggestion
        if sentiment > 0.3:
            st.success("🟢 Positive news sentiment — relevant for BUY consideration.")
        elif sentiment < -0.3:
            st.error("🔴 Negative sentiment — avoid for now.")
        else:
            st.info("🟡 Neutral sentiment — monitor further.")
