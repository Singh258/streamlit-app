import streamlit as st
import yfinance as yf
import pandas as pd
import io

# ---------- Page Setup ----------
st.set_page_config(page_title="Ritesh Stock Tracker", page_icon="📈", layout="wide")
st.title("📊 Ritesh Stock Price Dashboard")
st.markdown("Snapshot of stock prices with volume and daily stats. Powered by yfinance. Built for execution — no fallback.")

# ---------- Default Ticker List ----------
default_tickers = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "ITC.NS", "AXISBANK.NS", "LT.NS", "BHARTIARTL.NS"
]

# ---------- Ticker Input ----------
tickers_input = st.text_area("Enter stock tickers (comma-separated)", value=", ".join(default_tickers))
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

# ---------- Data Fetch Function ----------
@st.cache_data(show_spinner=False)
def fetch_stock_snapshot(ticker_list):
    snapshot = []
    for ticker in ticker_list:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            snapshot.append({
                "Ticker": ticker,
                "Price ₹": f"{info.get('regularMarketPrice', 'N/A'):.2f}" if info.get("regularMarketPrice") else "N/A",
                "Open": f"{info.get('open', 'N/A'):.2f}" if info.get("open") else "N/A",
                "Day High": f"{info.get('dayHigh', 'N/A'):.2f}" if info.get("dayHigh") else "N/A",
                "Day Low": f"{info.get('dayLow', 'N/A'):.2f}" if info.get("dayLow") else "N/A",
                "Volume": f"{info.get('volume', 'N/A'):,}" if info.get("volume") else "N/A"
            })
        except Exception as e:
            snapshot.append({
                "Ticker": ticker,
                "Price ₹": "Error",
                "Open": "Error",
                "Day High": "Error",
                "Day Low": "Error",
                "Volume": f"{str(e)}"
            })
    return pd.DataFrame(snapshot)

# ---------- Display Logic ----------
if tickers:
    df = fetch_stock_snapshot(tickers)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Please enter at least one valid stock ticker.")

# ---------- Export Section ----------
st.markdown("#### Export as CSV")
if 'df' in locals():
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button("📥 Download CSV", data=csv_buffer.getvalue(), file_name="stock_snapshot.csv", mime="text/csv")

# ---------- Footer ----------
st.markdown("---")
st.caption("App: Ritesh Stock Tracker · Engine: Streamlit + yfinance · Made for precision deployment")
