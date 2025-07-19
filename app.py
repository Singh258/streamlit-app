import streamlit as st
import yfinance as yf
from difflib import get_close_matches

st.set_page_config(page_title="Ritesh NSE Tracker", layout="centered")

@st.cache_data
def load_symbols():
    return ["RELIANCE", "TATAMOTORS", "SBIN", "ICICIBANK", "INFY", "HDFC", "ONGC", "ITC", "MARUTI", "LT"]

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
    for symbol in nse_symbols:
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
        info = yf.Ticker(symbol).info
        price = round(info.get("currentPrice", 0), 2)
        open_p = round(info.get("open", 0), 2)
        high = round(info.get("dayHigh", 0), 2)
        low = round(info.get("dayLow", 0), 2)
        prev = round(info.get("previousClose", 0), 2)
        change = round(price - prev, 2)
        percent = round((change / prev) * 100, 2) if prev != 0 else 0
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

st.markdown("<h2 style='text-align:center;'>Ritesh NSE Stock Tracker</h2>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Search Stock", "Browse Penny Stocks"])

with tab1:
    user_input = st.text_input("Type NSE symbol or name")
    resolved = resolve_symbol(user_input)
    if resolved:
        data = fetch_stock_data(resolved)
        if data:
            st.subheader(data["name"])
            if data["mode"] == "PRICE_ONLY":
                st.write(f"Price ₹{data['price']} | Change ₹{data['change']} ({data['percent']}%)")
            else:
                col1, col2, col3 = st.columns(3)
                col1.metric("Price ₹", data["price"], f"{data['change']} ({data['percent']}%)")
                col2.metric("Market Cap", f"₹{data['market_cap']} Cr")
                col3.metric("P/E", data["pe"])

                col4, col5, col6 = st.columns(3)
                col4.metric("ROCE", f"{data['roce']}%")
                col5.metric("Avg Price", f"₹{data['avg_price']}")
                col6.metric("Sentiment", data["sentiment"])

                st.write(f"Open: ₹{data['open']} | High: ₹{data['high']} | Low: ₹{data['low']}")
                st.write(f"Prev Close: ₹{data['prev_close']}")
                st.write(f"DMA 50: {data['dma_50']} | DMA 200: {data['dma_200']}")
                st.write(f"Trend: {data['trend']}")
        else:
            st.warning("Data fetch failed.")
    else:
        st.error("Symbol not found.")

with tab2:
    penny_list = get_below_50_stocks()
    if penny_list:
        selected = st.selectbox("Choose NSE stock under ₹50", penny_list)
        data = fetch_stock_data(selected + ".NS")
        if data:
            st.subheader(data["name"])
            col1, col2, col3 = st.columns(3)
            col1.metric("Price ₹", data["price"], f"{data['change']} ({data['percent']}%)")
            col2.metric("Market Cap", f"₹{data['market_cap']} Cr")
            col3.metric("P/E", data["pe"])

            col4, col5, col6 = st.columns(3)
            col4.metric("ROCE", f"{data['roce']}%")
            col5.metric("Avg Price", f"₹{data['avg_price']}")
            col6.metric("Sentiment", data["sentiment"])

            st.write(f"Open: ₹{data['open']} | High: ₹{data['high']} | Low: ₹{data['low']}")
            st.write(f"Prev Close: ₹{data['prev_close']}")
            st.write(f"DMA 50: {data['dma_50']} | DMA 200: {data['dma_200']}")
            st.write(f"Trend: {data['trend']}")
        else:
            st.warning("Data not available.")
    else:
        st.warning("No stocks found under ₹50.")











