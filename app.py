import streamlit as st
import yfinance as yf

st.set_page_config(page_title="📊 Ritesh NSE Stock App", layout="centered")

def fetch_stock(symbol):
    symbol = symbol.strip().upper()
    if not symbol.endswith(".NS"):
        symbol += ".NS"
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d", interval="1m")
        latest = hist.tail(1)
        if latest.empty:
            return None
        return {
            "symbol": symbol,
            "price": round(latest["Close"].iloc[0], 2),
            "high": round(latest["High"].iloc[0], 2),
            "low": round(latest["Low"].iloc[0], 2),
            "open": round(latest["Open"].iloc[0], 2),
            "volume": int(latest["Volume"].iloc[0])
        }
    except:
        return None

@st.cache_data(ttl=1800)
def get_penny_stocks():
    symbols = [
        "SUZLON.NS", "JPPOWER.NS", "IDEA.NS", "IRFC.NS", "NHPC.NS",
        "SJVN.NS", "IDFC.NS", "YESBANK.NS", "IOB.NS", "UNIONBANK.NS",
        "BANKBARODA.NS", "NBCC.NS", "GMRINFRA.NS", "PFC.NS", "BHEL.NS"
    ]
    result = []
    for sym in symbols:
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="1d", interval="1m")
            latest = hist.tail(1)
            if latest.empty:
                continue
            price = round(latest["Close"].iloc[0], 2)
            if 1 < price < 50:
                result.append({
                    "Symbol": sym,
                    "Price ₹": price,
                    "High ₹": round(latest["High"].iloc[0], 2),
                    "Low ₹": round(latest["Low"].iloc[0], 2),
                    "Volume": int(latest["Volume"].iloc[0])
                })
        except:
            continue
    return result

st.markdown("<h2 style='text-align:center;'>📈 NSE Stock Dashboard</h2>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🔍 Search Stock", "💸 Penny Stocks"])

with tab1:
    query = st.text_input("Enter NSE stock symbol (e.g. RELIANCE, TCS, SUZLON)")
    if query:
        data = fetch_stock(query)
        if data:
            st.success(f"Live data for {data['symbol']}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Price ₹", data["price"])
            col2.metric("High ₹", data["high"])
            col3.metric("Low ₹", data["low"])
            col4, col5 = st.columns(2)
            col4.metric("Open ₹", data["open"])
            col5.metric("Volume", f"{data['volume']:,}")
        else:
            st.error("⚠️ Could not fetch live data. Try again or check symbol.")

with tab2:
    penny = get_penny_stocks()
    if penny:
        st.subheader("Penny Stocks (Price under ₹50)")
        st.dataframe(penny, use_container_width=True)
    else:
        st.warning("⚠️ Penny stock data not available at the moment.")
    else:
        st.warning("⚠️ Could not fetch penny stock data.")


