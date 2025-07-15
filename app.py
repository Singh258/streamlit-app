import streamlit as st
import yfinance as yf
from nsepython import nse_eq

st.set_page_config(page_title="Ritesh Real Time Stock", layout="centered")

# 🔄 Load NSE symbol list
@st.cache_data
def load_symbols():
    try:
        data = nse_eq()
        return [item["symbol"].upper() for item in data]
    except:
        return []

nse_symbols = load_symbols()

# 📉 Filter below ₹50 stocks
@st.cache_data
def get_below_50_stocks():
    below_50 = []
    for symbol in nse_symbols[:500]:  # Limit for performance
        try:
            stock = yf.Ticker(symbol + ".NS")
            price = stock.info["currentPrice"]
            if price < 50:
                below_50.append(symbol)
        except:
            continue
    return sorted(below_50)

# 📊 Fetch metrics
def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")
        info = stock.info
        current = round(info["currentPrice"], 2)
        open_price = round(info["open"], 2)
        high = round(info["dayHigh"], 2)
        low = round(info["dayLow"], 2)
        prev_close = round(info["previousClose"], 2)
        change = round(current - prev_close, 2)
        percent = round((current - prev_close) / prev_close * 100, 2)
        avg_price = round((high + low + current) / 3, 2)
        delta = high - low
        trend = "Sideways" if delta < 0.3 else ("Uptrend" if current > open_price else "Downtrend")

        return {
            "name": info.get("longName", symbol),
            "price": current,
            "change": change,
            "percent": percent,
            "market_cap": round(info.get("marketCap", 0) / 1e7, 2),
            "pe": round(info.get("trailingPE", 0), 2),
            "roce": round(info.get("returnOnAssets", 0) * 100, 2),
            "open": open_price,
            "high": high,
            "low": low,
            "prev_close": prev_close,
            "avg_price": avg_price,
            "dma_50": "6.99 (mocked)",
            "dma_200": "7.88 (mocked)",
            "sentiment": "52.63% Sell (simulated)",
            "trend": trend
        }
    except:
        return None

# 🖼️ UI Layout
st.markdown("<h1 style='text-align:center; color:#1c3d5a;'>📉 Ritesh Real Time Stock</h1>", unsafe_allow_html=True)

show_list = st.button("🔎 Search Below ₹50 Stocks")

if show_list:
    below_50 = get_below_50_stocks()
    selected = st.selectbox("Select a stock under ₹50", below_50)

    data = fetch_stock_data(selected)
    if data:
        st.markdown(f"### 🔍 {data['name']}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Price ₹", data["price"], f"{data['change']} ({data['percent']}%)")
        col2.metric("Market Cap", f"₹{data['market_cap']} Cr")
        col3.metric("P/E Ratio", data["pe"])

        col4, col5, col6 = st.columns(3)
        col4.metric("ROCE", f"{data['roce']}%")
        col5.metric("Avg Price", f"₹{data['avg_price']}")
        col6.metric("Sentiment", data["sentiment"])

        st.markdown("### 📊 Trading Stats")
        st.write(f"Open: ₹{data['open']} | High: ₹{data['high']} | Low: ₹{data['low']}")
        st.write(f"Prev Close: ₹{data['prev_close']}")
        st.write(f"50 DMA: {data['dma_50']} | 200 DMA: {data['dma_200']}")
        st.write(f"Trend: **{data['trend']}**")
    else:
        st.warning("⚠️ Could not fetch data. Try another stock.")









