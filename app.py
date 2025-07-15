import streamlit as st
import yfinance as yf

def fetch_stock(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    hist = stock.history(period="1d", interval="5m")

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
        "avg_price": round(hist["Close"].mean(), 2),
        "trend": "Uptrend" if info["currentPrice"] > info["open"] else "Downtrend",
        "chart_data": hist["Close"]
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
        st.write(f"Prev Close: ₹{data['prev_close']} | Avg Price: ₹{data['avg_price']}")
        st.write(f"Trend: {data['trend']}")

    st.markdown("### 📊 Intraday Chart")
    st.line_chart(data["chart_data"])

symbol = st.text_input("🔎 Enter NSE Symbol (e.g. RELIANCE.NS, INFY.NS)", value="IDEA.NS")
if symbol:
    try:
        data = fetch_stock(symbol)
        render_card(data)
    except:
        st.error("⚠️ Data fetch failed. Try a valid symbol or check connectivity.")




