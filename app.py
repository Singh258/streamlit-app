import streamlit as st
import yfinance as yf

# Set page config for better layout
st.set_page_config(page_title="📊 Ritesh NSE Stock Tracker", layout="centered")

# 🟦 Function: Fetch live stock data for any NSE symbol
def fetch_stock(symbol):
    symbol = symbol.strip().upper()

    # Automatically append .NS if not present
    if not symbol.endswith(".NS"):
        symbol += ".NS"

    try:
        # Initialize ticker object
        ticker = yf.Ticker(symbol)

        # Fetch intraday historical data for today (1-minute interval)
        hist = ticker.history(period="1d", interval="1m")

        # Get the last entry (most recent data point)
        latest = hist.tail(1)

        # If data is empty, return None
        if latest.empty:
            return None

        # Extract values safely and return as dictionary
        return {
            "symbol": symbol,
            "price": round(latest["Close"].iloc[0], 2),
            "high": round(latest["High"].iloc[0], 2),
            "low": round(latest["Low"].iloc[0], 2),
            "open": round(latest["Open"].iloc[0], 2),
            "volume": int(latest["Volume"].iloc[0])
        }
    except Exception as e:
        return None  # In case of network issue or invalid symbol

# 🟩 Function: Get penny stocks (price < ₹50)
@st.cache_data(ttl=1800)  # Cache result for 30 minutes to avoid overload
def get_penny_stocks():
    # Shortlist of popular low-price NSE stocks
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
                continue  # Skip if no data

            price = round(latest["Close"].iloc[0], 2)

            # If price is under ₹50, include in list
            if 1 < price < 50:
                result.append({
                    "Symbol": sym,
                    "Price ₹": price,
                    "High ₹": round(latest["High"].iloc[0], 2),
                    "Low ₹": round(latest["Low"].iloc[0], 2),
                    "Volume": int(latest["Volume"].iloc[0])
                })
        except:
            continue  # Ignore exceptions for faulty symbols

    return result

# 🌟 Page layout begins
st.markdown("<h2 style='text-align:center;'>📈 NSE Stock Dashboard</h2>", unsafe_allow_html=True)

# ⬇️ Create tab structure
tab1, tab2 = st.tabs(["🔍 Search Stock", "💸 Penny Stocks"])

# 🔍 Tab 1: Individual Stock Search
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

# 💸 Tab 2: Penny Stock Screener
with tab2:
    penny = get_penny_stocks()
    if penny:
        st.subheader("📋 Penny Stocks (Price under ₹50)")
        st.dataframe(penny, use_container_width=True)
    else:
        st.warning("⚠️ Penny stock data not available at the moment.")


