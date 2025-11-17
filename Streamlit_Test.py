
# streamlit run Streamlit_Test2.py


import streamlit as st
import time
import requests
import json


# D:\Eddy\PythonProgs\Streamlit.streamlit\secrets.toml
# D:\Eddy\PythonProgs\Streamlit.streamlit\secrets.toml
#=====================================================================
#--- Program constants
GITHUB_GIST_FILENAME    = "JSON"

    # TTL / polling interval in seconden
RUN_EVERY = 2  # lager = snellere sync, maar meer requests

RV_SUCCESS = 0
RV_ERROR   = 1


GITHUB_TOKEN            = st.secrets["GITHUB_TOKEN"]
GITHUB_GIST_DESCRIPTION = st.secrets["GITHUB_GIST_DESCRIPTION"]
#st.write(st.secrets["GITHUB_TOKEN"])
#st.write(st.secrets["GITHUB_GIST_DESCRIPTION"])

#=====================================================================
# Create a Github gist with JSON data.
def Github_CreateGist_JSON(github_token, json_data, description, filename, public):
    '''
    Create a Github gist with JSON data.
    Input:
        - ..
        - public: False = private gist. True = public gist
    Output:
        - RetVal: RV_SUCCESS, RV_ERROR
        - gist_id
    '''
    
    # 🔹 API URL to create a Gist
    GIST_API_URL = "https://api.github.com/gists"

    # 🔹 Define the Gist content
    payload = {
        "description": description,
        "public": public,  # Set to False if you want a private Gist
        "files": {
            filename: {
                "content": json.dumps(json_data, indent=4)
            }
        }
    }

    # 🔹 Set up the headers with authentication
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 🔹 Make a POST request to create the Gist
    response = requests.post(GIST_API_URL, headers=headers, json=payload)
  
    # 🔹 Process the response
    gist_id = ''
    if response.status_code == 201:
        gist_url = response.json()["html_url"]
#         print(f"✅ Gist created successfully: {gist_url}")
        
        # Gebruik .get() voor veiligheid, voor het geval de sleutel niet bestaat
        gist_id = response.json().get('id','') 

#         print(f"Het Gist ID is: {gist_id}")
        RetVal = RV_SUCCESS
    else:
        print(f"❌ Failed to create Gist: {response.json()}")
        RetVal = RV_ERROR
        
    response.close()    
    return RetVal, gist_id   
#=====================================================================


#=====================================================================
def Github_Get_GistID(github_token, description):
    '''
    Given your Github token, and a description of your gist, this code
    searches the Gist ID of that gist (if it exists).
    Function returns a list with 0, 1 or more matches.
    
    Use an EMPTY STRING ('') as 'description' to find every possible Gist ID.
    'description' can also be a partial match and is case INsensitive: 'eddy' finds 'Eddys test'
    
    Input:
        - github_token
        - description: text string to identify Gist 
    Output:
        - Found: Number of Gist(s) that was found, that match the description.
        - Matches: List with the Gist ID's that were found (possibly empty)
    
    '''
    # ==== CONFIG ====
    API_URL = "https://api.github.com/gists"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json"
    }

    # Alle gists van de gebruiker ophalen (inclusief private)
    page = 1
    Found = 0
    matches = []

    while True:
        url = f"{API_URL}?page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Fout:", response.status_code, response.text)
            break

        gists = response.json()
        if not gists:
            break  # geen meer

        for gist in gists:
            desc = gist.get("description") or ""
            if description.lower() in desc.lower():  # case-insensitive zoek
                matches.append({
                    "id": gist.get("id"),
                    "description": desc,
                    "url": gist.get("html_url")
                })
        page += 1
        Found = len(matches)
        
    response.close()    
    return Found, matches    # Returns a list with 0, 1 or more matches
#=====================================================================


#=====================================================================
def Github_UpdateGist_JSON(github_token, gist_id, bestandsnaam, data): 
    '''
    Update data in Github JSON gist with known Gist_ID 
    Werkt de inhoud van een bestand in een GitHub Gist bij (CircuitPython-compatibel).
    'data' is een dictionary!

    Input:
        - github_token: Optional GitHub personal access token (needed for private gists)
        - gist_id
        - bestandsnaam: Naam van het bestand binnen de Gist. Case SENsitive en
          moet een exacte match zijn. Ofwel empty string, maar dan wordt een nieuw bestand
          aangemaakt.
        - data: Dictionary! de NIEUWE data van het bestand in de gist. Als je data wil toevoegen moet je
             vooraf de data uit de gist uitlezen. 'data' vervangt alle data in het bestand.
    Output:
        - RetVal: RV_SUCCESS, RV_ERROR
        - txt: Tekstinhoud van het bestand als string
    '''

    # CONVERTEER DICTIONARY NAAR JSON STRING
    # json.dumps(..., indent=4) zorgt voor een leesbare (pretty-printed) JSON-string.
    nieuwe_data_string = json.dumps(data, indent=4)
    #nieuwe_data_string = json.dumps(data)  #Circuitpython does not know 'indent'
    #nieuwe_data_string = JSON_str_pretty_print(data) #Alternatief voor "json.dumps(data)"
    
    
    RetVal, gist_json = Github_UpdateGist_Text(github_token, gist_id, bestandsnaam, nieuwe_data_string)
    
    return RetVal, gist_json    
#=====================================================================



#=====================================================================
def Github_UpdateGist_Text(github_token, gist_id, bestandsnaam, data): 
    '''
    Update a Github gist with text data.
    Werkt de inhoud van een bestand in een GitHub Gist bij (CircuitPython-compatibel).
    
    Deze functie gebruikt 'requests.patch()' NIET.
    MicroPython en Circuitpython kennen die method niet.
    Zie 'Github_UpdateGist_Text_V1()'als alternatief.  

    Input:
        - github_token: Optional GitHub personal access token (needed for private gists)
        - gist_id
        - bestandsnaam: Naam van het bestand binnen de Gist. Case SENsitive en
          moet een exacte match zijn. Ofwel empty string, maar dan wordt een nieuw bestand
          aangemaakt.
        - data: de NIEUWE data van het bestand in de gist. Als je data wil toevoegen moet je
             vooraf de data uit de gist uitlezen. 'data' vervangt alle data in het bestand.
    Output:
        - RetVal: RV_SUCCESS, RV_ERROR
        - gist_json: De bijgewerkte gist in json formaat.
    '''
    gist_json = ''
    url = "https://api.github.com/gists/" + gist_id
    headers = {
        "Authorization": "token " + github_token,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-HTTP-Method-Override": "PATCH"  # GitHub accepteert dit als PATCH
    }

    payload = {
        "files": {
            bestandsnaam: {"content": data}
        }
    }

    # Gebruik POST met header override (GitHub accepteert dit)
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code not in (200, 201):
        # Error
        print("Fout bij updaten Gist (status " + str(response.status_code) + "): " + response.text)
        RetVal = RV_ERROR
    else:    
        # Success
        gist_json = response.json()
        RetVal = RV_SUCCESS
        
    response.close() 
    return RetVal, gist_json    
#=====================================================================


#=====================================================================
# --- initialiseer de data slechts 1x per sessie ---
#     Alle data moet in st.session_state bewaard worden. Alle andere
#     data word gereset (gewist!) bij elke user-actie.
def Init_Data():
    # st.session_state is leeg. Initialiseer deze met de data uit de 'shared' data.
    # de 'shared' data wordt gedeeld tussen elke user die deze app gebruikt!
    st.session_state["group1"] = shared["group1"]
    st.session_state["group2"] = shared["group2"]
    
    # Houd bij welke versie van shared deze client laatst heeft gezien    
    st.session_state["time_data_last_seen"] = shared["time_data_last_updated"]   #0.0
    st.session_state.cntr = 0
    
    st.session_state["gist_id"] = ''
    Found, gists_found = Github_Get_GistID(GITHUB_TOKEN, GITHUB_GIST_DESCRIPTION)
    if Found == 0:
        # Gist not found. Create it.
        st.toast("Gist not found. Trying to create it", icon=":material/warning:", duration="short")
        
        # Store the data of 'shared' dictionary in it.
        GITHUB_GIST_FILENAME    = "JSON"
        public      = False    # Secret Gist
        RetVal, gist_id = Github_CreateGist_JSON(GITHUB_TOKEN, shared, GITHUB_GIST_DESCRIPTION, GITHUB_GIST_FILENAME, public)
        if RetVal == RV_SUCCESS:
            # Gist created succesfully
            st.session_state["gist_id"] = gist_id
            st.write("gist_id: ", gist_id)
            st.toast("Gist created succesfully!", icon=":material/thumb_up:", duration="short")
        else:
            st.toast("Could not create Gist!", icon=":material/disc_full:", duration="long")
            
    else:
        # Gist found
        st.toast("Gist found!", icon=":material/thumb_up:", duration="short")
        st.write(gists_found[0]['id'],'  --  ', gists_found[0]['description'])
        st.session_state["gist_id"] = gists_found[0]['id']   
    
    st.write("gist_id: ", st.session_state["gist_id"])
    return
#=====================================================================


#=====================================================================
# --- Gedeelde data ---
#     Deze data wordt gedeeld over alle verschillende open user-sessies. In verschillende browsers!
#     Dus als 1 user een setting wijzigt, ziet een ander user dit ook (vrijwel) meteen.
@st.cache_resource
def Get_Shared_State():
    # De data die hier gereturned wordt is de default data, indien er geen userdata beschikbaar zijn.
    # Als de user eenmaal selecties begint te maken, wordt deze data ge'update met de echte userdata.
    # Deze data wordt gedeeld tussen ALLE USERS die deze app gebruiken, op welk apparaat ook!
    # Het is de bedoeling dat, als 1 user iets wijzigt, dat de andere users deze wijziging zo snel
    # mogelijk te zijn krijgen op hun user interface.
    return {
        "group1": "opt1",
        "group2": "red",
        "time_data_last_updated": time.time(),
    }
#=====================================================================


   



#=====================================================================
def User_Action_Register():
    st.session_state.User_Action = True
    st.session_state.cntr += 1
    return
#=====================================================================

#=====================================================================
@st.fragment(run_every=RUN_EVERY)
def Page1_fragment():  #<-- This code is automatically run every RUN_EVERY seconds
     
    # --- Zorg dat widget states up to date zijn!!!
    # Indien er nieuwere shared data zijn (gewijzigd door een andere user),
    # sync deze naar deze session_state zodat de widgets zich aanpassen.
    # Dit overschrijft de widgets alleen wanneer er echt een *nieuwere* externe wijziging is.
    if shared["time_data_last_updated"] > st.session_state["time_data_last_seen"]:
        # Kopieer shared waarden naar deze sessie (zodat widgets de externe wijziging tonen)
        st.session_state["group1"] = shared["group1"]
        st.session_state["group2"] = shared["group2"]
        st.session_state["time_data_last_seen"] = shared["time_data_last_updated"]

    # --- Render widgets (koppelen aan session_state keys) ---
    # De widgets tonen de state, zoals opgeslagen in st.session_state (st.session_state["group1"]....)
    choice1 = st.radio(
        "Groep 1",
        options=["opt1", "opt2", "opt3"],
        key="group1",
        on_change = User_Action_Register,
    )

    choice2 = st.radio(
        "Groep 2",
        options=["red", "green", "blue"],
        key="group2",
        on_change = User_Action_Register,        
    )


    st.write('st.session_state.User_Action:',st.session_state.User_Action)
    if st.session_state.User_Action == True:
            
        st.session_state.User_Action = False
        st.write('st.session_state:',st.session_state["group1"],st.session_state["group2"])
#         st.write('do something here that takes some time',st.session_state.cntr)

#         st.session_state["group1"] = "opt1"  #<-- test

        shared["group1"] = st.session_state["group1"]
        shared["group2"] = st.session_state["group2"]
        
        shared["time_data_last_updated"] = time.time()
        # Deze client zag nu de nieuwste update (eigen wijziging)
        st.session_state["time_data_last_seen"] = shared["time_data_last_updated"]
        
        # Store changed data in Github Gist
        RetVal, resultaat = Github_UpdateGist_JSON(GITHUB_TOKEN, st.session_state["gist_id"], GITHUB_GIST_FILENAME, shared)
#         print(f'===RetVal===\n{RetVal}')
#         print(f'============\n{resultaat['html_url']}')
        if RetVal == RV_SUCCESS:
            st.toast("Modified data stored in Gist!", icon=":material/thumb_up:", duration="short")
        else:           
            st.toast("Could not store data in Gist!", icon=":material/disc_full:", duration="long")
            
#         time.sleep(5)        

#=====================================================================


#=====================================================================
#--- Main program
def here():
    pass

# App caption in browser
st.set_page_config(page_title="Eddys Home Control", page_icon="🔁")

# Create shared data dictionary (data is shared among all users/open sessions!!)
shared = Get_Shared_State()

st.session_state.User_Action = 0


# --- initialiseer de data slechts 1x per sessie ---
#     Alle data moet in st.session_state bewaard worden. Alle andere
#     data word gereset bij elke user-actie.
if "time_data_last_seen" not in st.session_state:
    # st.session_state is empty. Init it.
    Init_Data()
        
# Title on the 
st.title("🔁 Gedeelde radiobuttons")
 

# Start continuous loop        
Page1_fragment()  #<-- This code is automatically run every RUN_EVERY seconds

# # --- indicator / info buiten fragment ---
# delta = time.time() - shared["time_data_last_updated"]
# if delta < 4:
#     st.success("✅ Onlangs bijgewerkt door (andere) gebruiker")
# else:
#     st.info(f"Laatste wijziging {int(delta)} sec geleden")

# st.caption(f"Fragment herlaadt elke {RUN_EVERY} seconden (run_every). "



