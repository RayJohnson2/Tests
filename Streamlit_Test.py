
# streamlit run Streamlit_Test.py


import streamlit as st
import time

# --- gedeelde globale state (singleton voor de app) ---
@st.cache_resource
def get_shared_state():
    # eenvoudige dict; in productie gebruik je bijv. Redis/DB
    return {
        "group1": "opt1",
        "group2": "red",
        "last_update": time.time(),
    }

shared = get_shared_state()

st.set_page_config(page_title="Shared radios (fix)", page_icon="🔁")
st.title("🔁 Gedeelde radiobuttons (st.fragment run_every) - gefixt")

# Zorg dat we session_state keys alleen initialiseren als ze nog niet bestaan
if "group1_radio" not in st.session_state:
    st.session_state["group1_radio"] = shared["group1"]

if "group2_radio" not in st.session_state:
    st.session_state["group2_radio"] = shared["group2"]

@st.fragment(run_every=3)
def radios_fragment():
    # --- GROEP 1 ---
    # De widget 'key' is gekoppeld aan st.session_state["group1_radio"]
    choice1 = st.radio(
        "Groep 1",
        options=["opt1", "opt2", "opt3"],
        key="group1_radio",
        horizontal=False,
    )
    # Als de gebruiker een nieuwe keuze maakte (session_state != shared) -> update shared
    if st.session_state["group1_radio"] != shared["group1"]:
        shared["group1"] = st.session_state["group1_radio"]
        shared["last_update"] = time.time()

    st.markdown("---")

    # --- GROEP 2 ---
    choice2 = st.radio(
        "Groep 2",
        options=["red", "green", "blue"],
        key="group2_radio",
        horizontal=False,
    )
    if st.session_state["group2_radio"] != shared["group2"]:
        shared["group2"] = st.session_state["group2_radio"]
        shared["last_update"] = time.time()

radios_fragment()

# --- indicator / info buiten fragment ---
delta = time.time() - shared["last_update"]
if delta < 2:
    st.success("✅ Onlangs bijgewerkt door (andere) gebruiker")
else:
    st.info(f"Laatste wijziging {int(delta)} sec geleden")

st.caption("Fragment herlaadt elke 3 seconden (run_every=3). Voor productie: gebruik Redis/DB in plaats van cache_resource.")


