
# streamlit run Streamlit_Test2.py


import streamlit as st
import time

st.set_page_config(page_title="Eddys Home Control", page_icon="🔁")

# --- Gedeelde data ---
#     Deze data wordt gedeeld over alle verschillende open user-sessies. In verschillende browsers!
#     Dus als 1 user een setting wijzigt, ziet een ander user dit ook (vrijwel) meteen.
@st.cache_resource
def get_shared_state():
    # De data die hier gereturned wordt is de default data, indien er geen userdata beschikbaar zijn.
    # Als de user eenmaal selecties begint te maken, wordt deze data ge'update met de echte userdata.
    # Deze data wordt gedeeld tussen ALLE USERS die deze app gebruiken, op welk apparaat ook!
    # Het is de bedoeling dat, als 1 user iets wijzigt, dat de andere users deze wijziging zo snel
    # mogelijk te zijn krijgen op hun user interface.
    return {
        "group1": "opt1",
        "group2": "red",
        "last_update": time.time(),
    }

shared = get_shared_state()
st.session_state.User_Action = 0

st.title("🔁 Gedeelde radiobuttons")

# --- initialiseer de data slechts 1x per sessie ---
#     Alle data moet in st.session_state bewaard worden. Alle andere
#     data word gereset bij elke user-actie.
if "last_seen_shared_update" not in st.session_state:
    # st.session_state is leeg. Initialiseer deze met de data uit de 'shared' data.
    # de 'shared' data wordt gedeeld tussen elke user die deze app gebruikt!
    st.session_state["group1_radio"] = shared["group1"]
    st.session_state["group2_radio"] = shared["group2"]
    # Houd bij welke versie van shared deze client laatst heeft gezien    
    st.session_state["last_seen_shared_update"] = shared["last_update"]   #0.0
    st.session_state.cntr = 0    
    
    

# TTL / polling interval in seconden
RUN_EVERY = 2  # lager = snellere sync, maar meer requests

#==============================================
def User_Action_Register():
    st.session_state.User_Action = True
    st.session_state.cntr += 1
    return
#==============================================

#==============================================
@st.fragment(run_every=RUN_EVERY)
def radios_fragment():  #<-- This code is automatically run every RUN_EVERY seconds
     
    # --- Zorg dat widget states up to date zijn!!!
    # Indien er nieuwere shared data zijn (gewijzigd door een andere user),
    # sync deze naar deze session_state zodat de widgets zich aanpassen.
    # Dit overschrijft de widgets alleen wanneer er echt een *nieuwere* externe wijziging is.
    if shared["last_update"] > st.session_state["last_seen_shared_update"]:
        # Kopieer shared waarden naar deze sessie (zodat widgets de externe wijziging tonen)
        st.session_state["group1_radio"] = shared["group1"]
        st.session_state["group2_radio"] = shared["group2"]
        st.session_state["last_seen_shared_update"] = shared["last_update"]

    # --- Render widgets (koppelen aan session_state keys) ---
    # De widgets tonen de state, zoals opgeslagen in st.session_state (st.session_state["group1_radio"]....)
    choice1 = st.radio(
        "Groep 1",
        options=["opt1", "opt2", "opt3"],
        key="group1_radio",
        on_change = User_Action_Register,
    )

    choice2 = st.radio(
        "Groep 2",
        options=["red", "green", "blue"],
        key="group2_radio",
        on_change = User_Action_Register,        
    )


    st.write('st.session_state.User_Action:',st.session_state.User_Action)
    if st.session_state.User_Action == True:
            
        st.session_state.User_Action = False
        st.write('st.session_state:',st.session_state["group1_radio"],st.session_state["group2_radio"])
        st.write('do something here that takes some time',st.session_state.cntr)
        time.sleep(5)
#         st.session_state["group1_radio"] = "opt1"  #<-- test

        shared["group1"] = st.session_state["group1_radio"]
        shared["group2"] = st.session_state["group2_radio"]
        
        shared["last_update"] = time.time()
        # Deze client zag nu de nieuwste update (eigen wijziging)
        st.session_state["last_seen_shared_update"] = shared["last_update"]
        

#==============================================
        
radios_fragment()  #<-- This code is automatically run every RUN_EVERY seconds

# --- indicator / info buiten fragment ---
delta = time.time() - shared["last_update"]
if delta < 4:
    st.success("✅ Onlangs bijgewerkt door (andere) gebruiker")
else:
    st.info(f"Laatste wijziging {int(delta)} sec geleden")

# st.caption(f"Fragment herlaadt elke {RUN_EVERY} seconden (run_every). "


