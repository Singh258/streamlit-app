import streamlit as st
import yfinance as yf
from difflib import get_close_matches

st.set_page_config(page_title="Ritesh NSE Stock Hub", layout="centered")

@st.cache_data
def load_symbols():
    return [
        "RELIANCE", "TATAMOTORS", "SBIN", "ICICIBANK", "INFY", "HDFC", "ONGC", "ITC", "MARUTI", "LT", "SUZLON",
        "IDFC", "YESBANK", "BANKBARODA", "ASHOKLEY", "IDEA", "GMRINFRA", "NHPC", "IRFC", "JPPOWER", "SJVN"
    ]

nse_symbols = load_symbols()

def resolve_symbol(user_input):
    user_input = user_input.strip().upper().replace(".NS", "")
    if user_input in nse_symbols:
        return user_input + ".NS"
    fuzzy = get_close_matches(user_input, nse_symbols, n=1, cutoff=0.4)
    if fuzzy:
        return fuzzy[0] + ".NS"
    return None

@st.cache_data
def scan_penny_stocks(symbols):
    data = []
    for sym in symbols:
        try:
            info = yf.Ticker(sym + ".NS").info
            price = round(info.get("currentPrice", 0), 2)
            prev = round(info.get("previousClose", 0), 2)
            percent = round(((price - prev) / prev) * 100, 2) if prev else 0
            vol = info.get("volume", 0)
            cap = round(info.get("marketCap", 0) / 1e7, 2)
            pe = round(info.get("trailingPE", 0), 2)
            roce = round(info.get("returnOnAssets", 0) * 100, 2)
            if price < 50:
                data.append({
                    "Symbol": sym,
                    "Name": info.get("longName", sym),
                    "Price ₹": price,
                    "Change %": percent,
                    "Volume": vol,
                    "Market Cap": cap,
                    "P/E": pe,
                    "ROCE %": roce
                })
        except:
            continue
    return sorted(data, key=lambda x: x["Price ₹"])

def fetch_stock_data(sym):
    try:
        info = yf.Ticker(sym).info
        price = round(info.get("currentPrice", 0), 2)
        open_p = round(info.get("open", 0), 2)
        high = round(info.get("dayHigh", 0), 2)
        low = round(info.get("dayLow", 0), 2)
        prev = round(info.get("previousClose", 0), 2)
        change = round(price - prev, 2)
        percent = round((change / prev) * 100, 2) if prev else 0
        avg = round((price + high + low) / 3, 2)
        delta = round(high - low, 2)
        volatility = "Low" if delta < 1 else ("Medium" if delta < 3 else "High")
        trend = "Sideways" if delta < 0.5 else ("Uptrend" if price > open_p else "Downtrend")
        mood = "Entry Point" if price > avg and percent > 0 else ("Exit Point" if percent < 0 else "Neutral")

        return {
            "name": info.get("longName", sym),
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
            "volatility": volatility,
            "trend": trend,
            "signal": mood
        }
    except:
        return None

st.markdown("<h2 style='text-align:center;'>Ritesh NSE Research Hub</h2>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🔍 Search Stock", "📊 Browse Penny Stocks"])

with tab1:
    user_input = st.text_input("Enter NSE symbol or name")
    resolved = resolve_symbol(user_input)
    if resolved:
        data = fetch_stock_data(resolved)
        if data:
            st.subheader(data["name"])
            st.metric("Price ₹", data["price"], f"{data['change']} ({data['percent']}%)")
            st.write(f"Open: ₹{data['open']} | High: ₹{data['high']} | Low: ₹{data['low']}")
            st.write(f"Prev Close: ₹{data['prev_close']} | Avg: ₹{data['avg_price']}")
            st.write(f"Market Cap: ₹{data['market_cap']} Cr | P/E: {data['pe']} | ROCE: {data['roce']}%")
            st.write(f"Volatility: {data['volatility']} | Trend: {data['trend']}")
            st.success(f"📍 Signal: {data['signal']}")
        else:
            st.warning("⚠️ Data not available.")
    else:
        st.error("❌ Symbol not found.")

with tab2:
    penny = scan_penny_stocks(nse_symbols)
    if penny:
        st.subheader("Penny Stock List (Price < ₹50)")
        st.dataframe(penny, use_container_width=True)
        selected = st.selectbox("Select for detailed view", [p["Symbol"] for p in penny])
        detail = fetch_stock_data(selected + ".NS")
        if detail:
            st.subheader(detail["name"])
            col1, col2, col3 = st.columns(3)
            col1.metric("Price ₹", detail["price"], f"{detail['change']} ({detail['percent']}%)")
            col2.metric("Market Cap", f"₹{detail['market_cap']} Cr")
            col3.metric("P/E", detail["pe"])
            col4, col5, col6 = st.columns(3)
            col4.metric("ROCE", f"{detail['roce']}%")
            col5.metric("Avg Price", f"₹{detail['avg_price']}")
            col6.metric("Signal", detail["signal"])
            st.write(f"Open: ₹{detail['open']} | High: ₹{detail['high']} | Low: ₹{detail['low']}")
            st.write(f"Prev Close: ₹{detail['prev_close']} | Volatility: {detail['volatility']}")
            st.write(f"Trend: {detail['trend']}")
        else:
            st.warning("⚠️ Data fetch failed.")
    else:
        st.info("No penny stocks found.")
