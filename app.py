import streamlit as st
import requests

# --- UI Setup ---
st.set_page_config(page_title="Indian Stock Screener", layout="centered")
st.title("📈 Indian Stock Market Insights")

# --- Helper Function ---
def fetch_stock_data(stock_name):
    url = f"https://indianapi.in/api/stock?name={stock_name}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

# --- User Input ---
stock_query = st.text_input("🔍 Enter Stock Name (e.g., Reliance, TCS, Suzlon)")
if stock_query:
    result = fetch_stock_data(stock_query)
    
    if "error" in result or "currentPrice" not in result:
        st.error("⚠️ Unable to fetch data. Check stock name or try again later.")
    else:
        st.subheader(f"📊 {result['companyName']} ({result['tickerId']})")
        price = result["currentPrice"]["NSE"]
        high = result["yearHigh"]
        low = result["yearLow"]
        volume = result["volume"]
        change = result["percentChange"]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Price (₹)", f"{price}")
        col2.metric("Day Change (%)", f"{change}")
        col3.metric("52W High", f"{high}")
        col4.metric("52W Low", f"{low}")

        st.caption("📅 Data fetched from Indian Stock Exchange API")

        # --- Optional News Section ---
        if "recentNews" in result and result["recentNews"]:
            st.subheader("📰 Recent News")
            for news in result["recentNews"][:3]:
                st.markdown(f"- [{news['title']}]({news['link']})")

