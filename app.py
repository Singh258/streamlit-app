import streamlit as st
import yfinance as yf

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info

    return {
        "name": info.get("longName", symbol),
        "price": round(info["currentPrice"], 2),
        "change": round(info["currentPrice"] - info["previousClose"], 2),
        "percent_change": round(((info["currentPrice"] - info["previousClose"]) / info["previousClose"]) * 100, 2),
        "market_cap": round(info.get("marketCap", 0) / 1e7, 2),
        "pe_ratio": round(info.get("trailingPE", 0), 2),
        "open": round(info.get("open", 0), 2),
        "high": round(info.get("dayHigh", 0), 2),
        "low": round(info.get("dayLow", 0), 2),
        "prev_close": round(info.get("previousClose", 0), 2),
        "avg_price": None,  # Removed graph so no historical fetch
        "trend": "Uptrend" if info["currentPrice"] > info["open"] else "Downtrend"
    }

def render_card(data):
    st.set_page_config(page_title="📈 Ritesh Real Time Stock", layout="wide")
    st.title("📈 Ritesh Real Time Stock")
    st.markdown(f"### 🏷️ {data['name']}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Price (₹)", data["price"], f"{data['change']} ({data['percent_change']}%)")
    col2.metric("Market Cap", f'₹{data["market_cap"]} Cr')
    col3.metric("P/E Ratio", data["pe_ratio"])

    with st.expander("🔍 More Stats"):
        st.write(f"Open: ₹{data['open']} | High: ₹{data['high']} | Low: ₹{data['low']}")
        st.write(f"Prev Close: ₹{data['prev_close']}")
        st.write(f"Trend: {data['trend']}")

symbol = st.text_input("🔎 Enter NSE Symbol (e.g. RELIANCE.NS, INFY.NS)", value="IDEA.NS")
if symbol:
    try:
        stock_data = fetch_stock_data(symbol)
        render_card(stock_data)
    except:
        st.error("⚠️ Data fetch failed. Try a valid symbol or check connectivity.")





