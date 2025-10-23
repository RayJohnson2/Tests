
# streamlit run Streamlit_Test.py

import streamlit as st
import time

# --- TIMER VOOR AUTO-REFRESH ---
REFRESH_INTERVAL = 3  # seconden

if "last_client_refresh" not in st.session_state:
    st.session_state.last_client_refresh = time.time()

if time.time() - st.session_state.last_client_refresh > REFRESH_INTERVAL:
    st.session_state.last_client_refresh = time.time()
    st.rerun()

# --- SHARED STATE (GLOBAAL) ---
@st.cache_resource
def get_shared_state():
    return {
        "group1": "opt1",
        "group2": "red",
        "last_update": time.time()
    }

shared = get_shared_state()

st.title("🔄 Real-time gedeelde radiobuttons demo")

# -----------------------------
# GROEP 1
# -----------------------------
choice1 = st.radio(
    "Groep 1",
    options=["opt1", "opt2", "opt3"],
    index=["opt1", "opt2", "opt3"].index(shared["group1"])
)

if choice1 != shared["group1"]:
    shared["group1"] = choice1
    shared["last_update"] = time.time()
    st.rerun()

# -----------------------------
# GROEP 2
# -----------------------------
choice2 = st.radio(
    "Groep 2",
    options=["red", "green", "blue"],
    index=["red", "green", "blue"].index(shared["group2"])
)

if choice2 != shared["group2"]:
    shared["group2"] = choice2
    shared["last_update"] = time.time()
    st.rerun()

# -----------------------------------------
# VISUELE INDICATOR wanneer andere sessie updatet
# -----------------------------------------
delta = time.time() - shared["last_update"]

if delta < 2:
    st.success("✅ Update ontvangen van andere gebruiker (net gewijzigd!)")
else:
    st.info(f"Laatste wijziging {int(delta)} sec geleden")

st.caption("Deze pagina refresh automatisch elke 3 seconden voor synchronisatie.")

