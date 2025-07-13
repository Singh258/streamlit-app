import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# 📅 Date Range
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

# 🔑 API Keys — replace with actual values
ALPHA_VANTAGE_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
MARKETAUX_KEY = "YOUR_MARKETAUX_API_KEY"

# 🔧 Streamlit Config
st.set_page_config(page_title="RK Stock Center", layout="centered")
st.title("RK Stock Center 📈")
st.subheader("Real-time Penny Stock Screener with AI News Relevance")

# 📌 Symbol Input
symbol = st.text_input("Enter penny stock symbol (e.g. IDEA.BSE)", max_chars=12)

# 🔍 Functions
def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    try:
        res = requests.get(url)
        data = res.json().get("Time Series (Daily)", {})
        df = pd.DataFrame.from_dict(data, orient="index")
        df = df.rename(columns={"4. close": "Close"})
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df = df.sort_index().tail(30)
        return df["Close"]
    except Exception:
        return None

def fetch_news_sentiment(symbol):
    url = f"https://api.marketaux.com/v1/news/all?symbols={symbol}&filter_entities=true&language=en&api_token={MARKETAUX_KEY}"
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

