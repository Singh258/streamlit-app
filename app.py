import streamlit as st
import yfinance as yf
from difflib import get_close_matches
from nsepython import nse_eq

st.set_page_config(page_title="Ritesh Real Time Stock", layout="centered")

@st.cache_data
def load_symbols():
    try:
        data = nse_eq()
        return [item["symbol"].upper() for item in data]
    except:
        return []

nse_symbols = load_symbols()

def resolve_symbol(user_input):
    user_input = user_input.strip().upper().replace(".NS", "")
    if user_input in nse_symbols:
        return user_input + ".NS"
    static_map = {
        "RELIANCE": "RELIANCE.NS",
        "TATAMOTORS": "TATAMOTORS.NS",
        "SBIN": "SBIN.NS",
        "ICICIBANK": "ICICIBANK.NS",
        "HDFC": "HDFC.NS",
        "INFY": "INFY.NS"
    }
    if user_input in static_map:
        return static_map[user_input]
    fuzzy = get_close_matches(user_input, nse_symbols, n=1, cutoff=0.4)
    if fuzzy:
        return fuzzy[0] + ".NS"
    return None

def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        current = round(info["currentPrice"], 2)
        open_price = round(info["open"], 2)
        high = round(info["dayHigh"], 2)
        low = round(info["dayLow"], 2)
        prev_close = round(info["previousClose"], 2)
        change = round(current - prev_close, 2)
        percent = round(((current - prev_close) / prev_close) * 100, 2)
        delta = high - low
        trend = "Sideways" if delta < 0.3 else ("Uptrend" if current > open_price else "Downtrend")

        if current > 50:
            return {
                "name": info.get("longName", symbol),
                "price": current,
                "change": change,
                "percent": percent,
                "mode": "PRICE_ONLY"
            }
        else:
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
                "avg_price": round((high + low + current) / 3, 2),
                "dma_50": "6.99 (mocked)",
                "dma_200": "7.88 (mocked)",
                "sentiment": "52.63% Sell (simulated)",
                "trend": trend,
                "mode": "FULL"
            }
    except:
        return None

st.markdown("<h1 style='text-align:center; color:#1c3d5a;'>📉 Ritesh Real Time Stock (₹50 Below: Full, ₹50+ Price Only)</h1>", unsafe_allow_html=True)
user_input = st.text_input("🔍 Enter NSE stock name", value="jp power")
resolved = resolve_symbol(user_input)

if resolved:
    data = fetch_stock_data(resolved)
    if data:
        st.markdown(f"### 🔍 {data['name']}")
        if data["mode"] == "PRICE_ONLY":
            st.success(f"💰 Price: ₹{data['price']} | Change: {data['change']} ({data['percent']}%)")
            st.info("ℹ️ This is a high-value stock. Showing price only.")
        else:
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
        st.error("❌ Data fetch failed. Try again or check symbol.")
else:
    st.error("❌ Symbol not recognized. Check spelling or use valid NSE stock name.")








