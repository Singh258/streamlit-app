import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Ritesh Real Time Stock", layout="centered")

def fetch_stock(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        current = round(info["currentPrice"], 2)
        open_price = round(info["open"], 2)
        high = round(info["dayHigh"], 2)
        low = round(info["dayLow"], 2)
        avg_price = round((high + low + current) / 3, 2)
        prev_close = round(info["previousClose"], 2)

        # Trend Analysis
        delta = high - low
        trend = "Sideways" if delta < 0.3 else ("Uptrend" if current > open_price else "Downtrend")

        return {
            "name": info.get("longName", symbol),
            "price": current,
            "change": round(current - prev_close, 2),
            "percent": round(((current - prev_close) / prev_close) * 100, 2),
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

st.markdown("<h1 style='text-align:center; color:#1c3d5a;'>📈 Ritesh Real Time Stock</h1>", unsafe_allow_html=True)
symbol = st.text_input("🔍 Enter NSE Symbol (e.g. IDEA.NS)", value="IDEA.NS")

if symbol:
    data = fetch_stock(symbol)
    if data:
        st.markdown("""
            <div style='background-color:#f4f8fd; padding:25px; border-radius:15px; margin-top:20px; box-shadow:0 4px 12px rgba(0,0,0,0.1);'>
        """, unsafe_allow_html=True)

        st.markdown(f"<h3 style='color:#1c3d5a;'>{data['name']}</h3>", unsafe_allow_html=True)

        # Primary Metrics Panel
        col1, col2, col3 = st.columns(3)
        col1.metric("Price ₹", data["price"], f"{data['change']} ({data['percent']}%)")
        col2.metric("Market Cap", f"₹{data['market_cap']} Cr")
        col3.metric("P/E Ratio", data["pe"])

        # Secondary Panel
        col4, col5, col6 = st.columns(3)
        col4.metric("ROCE", f"{data['roce']}%")
        col5.metric("Avg Traded Price", f"₹{data['avg_price']}")
        col6.metric("Sentiment", data["sentiment"])

        # Stats Section
        st.markdown("### 📊 Trading Stats")
        st.write(f"Open: ₹{data['open']} | High: ₹{data['high']} | Low: ₹{data['low']}")
        st.write(f"Previous Close: ₹{data['prev_close']}")
        st.write(f"50 DMA: {data['dma_50']} | 200 DMA: {data['dma_200']}")
        st.write(f"Trend: **{data['trend']}**")

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background-color:#fff3cd; padding:20px; border-radius:12px; border-left:6px solid #ffdd57; margin-top:20px;'>
            <strong>⚠️ Data not available.</strong><br>Please check the symbol or try again later.
            </div>
        """, unsafe_allow_html=True)








