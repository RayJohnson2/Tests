import streamlit as st
import time
from streamlit_option_menu import option_menu

# import pandas as pd
# import numpy as np
# from datetime import date, time

# streamlit run Streamlit_HomeControl1.py

st.session_state.update(st.session_state)

#st.title ("_Eddy's_ Home Control :house:")
# st.header("_Eddy's_ Home Control :house:")

# @st.fragment(run_every="5s")
@st.cache_data(ttl=5)  # ververs cache elke x seconden
def mijn_langzame_functie():
#     st.write("Functie wordt uitgevoerd...")
    # Je langdurige code hier
    time.sleep(2)  # simulatie
    st.write(f"Laatste update: {time.strftime('%H:%M:%S')}")

# mijn_langzame_functie()

# # Check if the variable 'counter' exists in the session state
# if 'start_function' not in st.session_state:
#     st.write('start_function not in st.session_state')
#     # If not, initialize it (this happens only on the very first load)
#     st.session_state['start_function'] = 1
#     mijn_langzame_functie()
    
# st.subheader("Selecteer het weertype :sunglasses:")
options = ["🌞Zonnig", "⛅️ Wisselvallig", "☔️Bewolkt"]
selection = st.pills("Selecteer het weertype :sunglasses:", options, selection_mode="single")
st.markdown(f"Het is vandaag: {selection}.")

options = ["🌞Zonnig", "⛅️ Wisselvallig", "☔️Bewolkt"]
selection = st.segmented_control(
    "Selecteer het weertype :sunglasses:", options, selection_mode="single"
)
# st.markdown(f"Your selected options: {selection}.")


# # De opties die u normaal in st.pills zou gebruiken
# keuze_opties = ["🚗 Auto", "🚀 Vliegtuig", "🚂 Trein", "🚲 Fiets"]
# 
# # Gebruik st.radio voor de verticale lay-out
# # De 'index' stelt de standaard geselecteerde optie in.
# gekozen_optie = st.radio(
#     "Kies uw vervoersmiddel:",
#     options=keuze_opties,
#     index=0,  # Standaard is 'Auto'
#     key='vervoer_keuze'
# )
# st.info(f"U heeft gekozen voor: **{gekozen_optie}**")



selected = option_menu(
    "Batterij mode",
    ["Home", "Instellingen", "Over"],
    icons=["house", "gear", "info-circle"],  # Bootstrap icons
    orientation="vertical",
    styles={
        "nav-link": {
            "font-size": "16px",
            "border-radius": "10px",
            "margin-bottom": "5px",
        },
        "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
    }
)

st.write("Geselecteerde optie:", selected)

# st.divider()  # 👈 Draws a horizontal rule

mijn_langzame_functie()

