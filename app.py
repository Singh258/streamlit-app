import streamlit as st
import yfinance as yf
from nsepython import nse_eq
from difflib import get_close_matches

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

@st.cache_data
def get_below_50_stocks():
    result = []
    for symbol in nse_symbols[:1000]:  # limit for performance
        try:
            info = yf.Ticker(symbol + ".NS").info
            price = info.get("currentPrice", 0)
            if price and price < 50:
                result.append(symbol)
        except:
            continue
    return sorted(result)

def fetch_stock_data(symbol):
    try:
        info = yf.Ticker(symbol + ".NS").info
        price = round(info["currentPrice"], 2)
        open_p = round(info["open"], 2)
        high = round(info["dayHigh"], 2)
        low = round(info["dayLow"], 2)
        prev = round(info["previousClose"], 2)
        change = round(price - prev, 2)
        percent = round((change / prev) * 100, 2)
        avg = round((price + high + low) / 3, 2)
        delta = high - low
        trend = "Sideways" if delta < 0.3 else ("Uptrend" if price > open_p else "Downtrend")

        if price > 50:
            return {
                "name": info.get("longName", symbol),
                "price": price,
                "change": change,
                "percent": percent,
                "mode": "PRICE_ONLY"
            }

        return {
            "name": info.get("longName", symbol),
            "price": price,
            "change": change,
            "percent": percent,
            "market_cap": round(info.get("marketCap", 0) / 1e7, 2),
            "pe": round(info.get("trailingPE", 0), 2),
            "roce": round(info.get("returnOnAssets", 0) * 100, 2),
            "open": open_p,
            "high": high,
            "low": low,
            "prev_close": prev,
            "avg_price": avg,
            "dma_50": "6.99 (mocked)",
            "dma_200": "7.88 (mocked)",
            "sentiment": "52.63% Sell (simulated)",
            "trend": trend,
            "mode": "FULL"
        }
    except:
        return None

# 🖼️ UI Layout
st.markdown("<h1 style='text-align:center; color:#1c3d5a;'>📉 Ritesh Real Time Stock</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔎 Search Input", "📋 Browse Penny Stocks"])

# Tab 1 – Search box
with tab1:
    user_input = st.text_input("Type stock name (e.g. idea, jp power)", value="jp power")
    resolved = resolve_symbol(user_input)
    if resolved:
        data = fetch_stock_data(resolved)
        if data:
            st.markdown(f"### 🔍 {data['name']}")
            if data["mode"] == "PRICE_ONLY":
                st.success(f"💰 Price: ₹{data['price']} | Change: {data['change']} ({data['percent']}%)")
                st.info("ℹ️ High-value stock. Showing price only.")
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
            st.warning("⚠️ Data fetch failed. Try again.")
    else:
        st.error("❌ Symbol not recognized. Check spelling.")

# Tab 2 – Browse button
with tab2:
    below_50 = get_below_50_stocks()
    if below_50:
        selected = st.selectbox("Select NSE stock under ₹50", below_50)
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
            st.warning("⚠️ Data not found for selection.")
    else:
        st.warning("⚠️ No penny stocks found in NSE data. Check connection or try later.")









