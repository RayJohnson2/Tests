import streamlit as st
from streamlit_option_menu import option_menu

# import pandas as pd
# import numpy as np
# from datetime import date, time

# streamlit run Streamlit_HomeControl1.py

#st.title ("_Eddy's_ Home Control :house:")
st.header("_Eddy's_ Home Control :house:")

st.subheader("Selecteer het weertype :sunglasses:")
options = ["🌞Zonnig", "⛅️ Wisselvallig", "☔️Bewolkt"]
selection = st.pills("Weertype", options, selection_mode="single")
st.markdown(f"Het is vandaag: {selection}.")

options = ["🌞Zonnig", "⛅️ Wisselvallig", "☔️Bewolkt"]
selection = st.segmented_control(
    "Weertype", options, selection_mode="single"
)
st.markdown(f"Your selected options: {selection}.")


# De opties die u normaal in st.pills zou gebruiken
keuze_opties = ["🚗 Auto", "🚀 Vliegtuig", "🚂 Trein", "🚲 Fiets"]

# Gebruik st.radio voor de verticale lay-out
# De 'index' stelt de standaard geselecteerde optie in.
gekozen_optie = st.radio(
    "Kies uw vervoersmiddel:",
    options=keuze_opties,
    index=0,  # Standaard is 'Auto'
    key='vervoer_keuze'
)

st.info(f"U heeft gekozen voor: **{gekozen_optie}**")



selected = option_menu(
    "Maak een keuze",
    ["Optie 1", "Optie 2", "Optie 3"],
    orientation="vertical",  # maakt ze verticaal
    styles={
        "container": {"padding": "10px"},
        "nav-link": {
            "font-size": "16px",
            "border-radius": "10px",
            "text-align": "left",
            "margin-bottom": "5px",
        },
        "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
    }
)

st.write("Geselecteerd:", selected)

st.divider()  # 👈 Draws a horizontal rule
