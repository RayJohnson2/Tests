import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, time

# streamlit run Streamlit_HomeControl1.py

st.title("_Eddy's_ Home Control :house:")
st.subheader("Selecteer het weertype :sunglasses:")
options = ["🌞Zonnig", "⛅️ Wisselvallig", "☔️Bewolkt"]
selection = st.pills("Weertype", options, selection_mode="single")
st.markdown(f"Het is vandaag: {selection}.")

options = ["🌞Zonnig", "⛅️ Wisselvallig", "☔️Bewolkt"]
selection = st.segmented_control(
    "Weertype", options, selection_mode="single"
)
st.markdown(f"Your selected options: {selection}.")
st.divider()  # 👈 Draws a horizontal rule
