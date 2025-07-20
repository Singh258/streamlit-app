import streamlit as st
import yfinance as yf

# 👇 Set up page layout and title for Streamlit app
st.set_page_config(page_title="📊 Ritesh NSE Stock Tracker", layout="centered")

# 🚀 Function to fetch real-time data for a single NSE stock
def fetch_stock(symbol):
    # 🔍 Clean and format user input
    symbol = symbol.strip().upper()
    if not symbol.endswith(".NS"):  # Ensure it's in NSE format
        symbol += ".NS"

    try:
        # 📡 Create ticker object using yfinance
        ticker = yf.Ticker(symbol)

        # 🕒 Fetch latest intraday historical data (1-minute resolution)
        hist = ticker.history(period="1d", interval="1m")

        # 📦 Extract the most recent data point
        latest = hist.tail(1)

        # ⚠️ If no data is returned, consider it unavailable
        if latest.empty:
            return None

        # ✅ If data exists, format it into dictionary
        return {
            "symbol": symbol,
            "price": round(latest["Close"].iloc[0], 2),
            "high": round(latest["High"].iloc[0], 2),
            "low": round(latest["Low"].iloc[0], 2),
            "open": round(latest["Open"].iloc[0], 2),
            "volume": int(latest["Volume"].iloc[0])
        }
    except Exception as e:
        # 🛑 Any error (network, symbol, library) returns None
        return None

# 💸 Function to get list of penny stocks under ₹50
@st.cache_data(ttl=1800)  # ⏱️ Cache for 30 mins to reduce API load
def get_penny_stocks():
    # 📋 Predefined symbols commonly considered penny stocks
    penny_symbols = [
        "SUZLON.NS", "JPPOWER.NS", "IDEA.NS", "IRFC.NS", "NHPC.NS",
        "SJVN.NS", "IDFC.NS", "YESBANK.NS", "IOB.NS", "UNIONBANK.NS",
        "BANKBARODA.NS", "NBCC.NS", "GMRINFRA.NS", "PFC.NS", "BHEL.NS"
    ]

    result = []

    for sym in penny_symbols:
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="1d", interval="1m")
            latest = hist.tail(1)

            if latest.empty:
                continue  # ❌ Skip symbol if no data found

            price = round(latest["Close"].iloc[0], 2)

            # ✅ Only include stocks under ₹50
            if 1 < price < 50:
                result.append({
                    "Symbol": sym,
                    "Price ₹": price,
                    "High ₹": round(latest["High"].iloc[0], 2),
                    "Low ₹": round(latest["Low"].iloc[0], 2),
                    "Volume": int(latest["Volume"].iloc[0])
                })
        except Exception:
            continue  # ❌ If error, skip symbol

    # 📦 Return full penny stock list
    return result

# 🎨 Build Streamlit UI layout
st.markdown("<h2 style='text-align:center;'>📈 NSE Stock Dashboard</h2>", unsafe_allow_html=True)

# 📊 Two tabs for user interaction
tab1, tab2 = st.tabs(["🔍 Search Stock", "💸 Penny Stocks"])

# 🔍 Tab 1 — Search any NSE stock symbol and show live data
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

# 💸 Tab 2 — Show penny stocks under ₹50 with full metrics
with tab2:
    penny = get_penny_stocks()

    if penny:
        st.subheader("📋 Penny Stocks (Below ₹50)")
        st.dataframe(penny, use_container_width=True)
    else:
        st.warning("⚠️ Penny stock data not available at the moment.")


