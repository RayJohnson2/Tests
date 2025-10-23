
# streamlit run Streamlit_Test.py


import streamlit as st
import time

st.set_page_config(page_title="Shared radios (robust sync)", page_icon="🔁")

# --- gedeelde globale state (singleton voor de app) ---
# In productie: gebruik Redis/Postgres/Firestore voor cross-instance sync.
@st.cache_resource
def get_shared_state():
    return {
        "group1": "opt1",
        "group2": "red",
        "last_update": time.time(),
    }

shared = get_shared_state()

st.title("🔁 Gedeelde radiobuttons (run_every sync, verbeterd)")

# --- initialiseer's session_state keys slechts 1x per sessie ---
if "group1_radio" not in st.session_state:
    st.session_state["group1_radio"] = shared["group1"]

if "group2_radio" not in st.session_state:
    st.session_state["group2_radio"] = shared["group2"]

# Houd bij welke versie van shared deze client laatst heeft gezien
if "last_seen_shared_update" not in st.session_state:
    st.session_state["last_seen_shared_update"] = 0.0

# TTL / polling interval in seconden
RUN_EVERY = 2  # lager = snellere sync, maar meer requests

@st.fragment(run_every=RUN_EVERY)
def radios_fragment():
    # --- Indien er een nieuwere shared-update is: sync naar session_state ---
    # Dit overschrijft de widgets alleen wanneer er echt een *nieuwere* externe wijziging is.
    if shared["last_update"] > st.session_state["last_seen_shared_update"]:
        # Kopieer shared waarden naar deze sessie (zodat widgets de externe wijziging tonen)
        st.session_state["group1_radio"] = shared["group1"]
        st.session_state["group2_radio"] = shared["group2"]
        st.session_state["last_seen_shared_update"] = shared["last_update"]

    # --- Render widgets (koppelen aan session_state keys) ---
    choice1 = st.radio(
        "Groep 1",
        options=["opt1", "opt2", "opt3"],
        key="group1_radio",
    )

    # Als gebruiker iets wijzigt -> update shared en markeer last_update
    if st.session_state["group1_radio"] != shared["group1"]:
        shared["group1"] = st.session_state["group1_radio"]
        shared["last_update"] = time.time()
        # Deze client zag nu de nieuwste update (eigen wijziging)
        st.session_state["last_seen_shared_update"] = shared["last_update"]

    st.markdown("---")

    choice2 = st.radio(
        "Groep 2",
        options=["red", "green", "blue"],
        key="group2_radio",
    )

    if st.session_state["group2_radio"] != shared["group2"]:
        shared["group2"] = st.session_state["group2_radio"]
        shared["last_update"] = time.time()
        st.session_state["last_seen_shared_update"] = shared["last_update"]

radios_fragment()

# --- indicator / info buiten fragment ---
delta = time.time() - shared["last_update"]
if delta < 2:
    st.success("✅ Onlangs bijgewerkt door (andere) gebruiker")
else:
    st.info(f"Laatste wijziging {int(delta)} sec geleden")

st.caption(f"Fragment herlaadt elke {RUN_EVERY} seconden (run_every). "
           "Voor productie: gebruik Redis/DB zodat state gedeeld is tussen meerdere server-instanties.")


