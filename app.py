import streamlit as st
from nsepy import get_history
from datetime import date

st.title("📊 Stock Data Viewer")

symbol = st.selectbox("Choose Stock", ["RELIANCE", "TCS", "INFY", "HDFCBANK"])
start = st.date_input("Start Date", value=date(2024, 1, 1))
end = st.date_input("End Date", value=date.today())
if start > end:
    st.warning("Start date cannot be after end date!")

if st.button("Fetch Data"):
    try:
        data = get_history(symbol=symbol, start=start, end=end)
        st.dataframe(data)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
