import streamlit as st

st.title("RK stock!")
st.write("Yeh Ritesh k stock center hai powered by RK.")
from nsepy import get_history
from datetime import date

data = get_history(symbol="RELIANCE", start=date(2024,1,1), end=date(2024,7,1))
st.write(data.tail())
