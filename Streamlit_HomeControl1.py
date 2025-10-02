import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, time

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("⚙️ Instellingen")
st.sidebar.write("Hier kun je opties kiezen die invloed hebben op de app.")

sidebar_choice = st.sidebar.radio(
    "Kies een pagina:", 
    ["Overzicht", "Formulier", "Grafieken", "Data", "Widgets"]
)
show_code = st.sidebar.checkbox("Laat code zien", value=True)

# ----------------------------
# PAGINA: OVERZICHT
# ----------------------------
if sidebar_choice == "Overzicht":
    st.title("🎨 Streamlit Feature Demo")
    st.write("Welkom bij de demo-app! Hier laten we zoveel mogelijk **Streamlit-widgets** zien.")
    st.success("✅ Je gebruikt Streamlit!")
    st.info("ℹ️ Klik links in de sidebar om te navigeren.")
    st.warning("⚠️ Vergeet niet dat dit een demo is.")
    st.error("❌ Dit is een voorbeeld error-bericht.")

    st.markdown("""
    ### 📋 Features in deze app
    - Widgets (knoppen, sliders, tekstvelden, selecties, etc.)
    - Media (afbeeldingen, audio, video, iconen via emoji)
    - Dataframes en tabellen
    - Grafieken (Streamlit built-in charts)
    - Statusmeldingen en lay-out
    """)

# ----------------------------
# PAGINA: FORMULIER
# ----------------------------
elif sidebar_choice == "Formulier":
    st.header("📝 Formulier Demo")

    with st.form("mijn_form"):
        naam = st.text_input("Wat is je naam?")
        leeftijd = st.number_input("Wat is je leeftijd?", 0, 120, 25)
        geboortedatum = st.date_input("Geboortedatum", date(1990, 1, 1))
        tijd = st.time_input("Voorkeurstijd", time(12, 0))
        kleur = st.color_picker("Kies je favoriete kleur", "#00f900")
        akkoord = st.checkbox("Ik ga akkoord met de voorwaarden")
        submit = st.form_submit_button("Verstuur")

    if submit:
        st.success(f"Hallo {naam}, je bent {leeftijd} jaar oud!")
        st.write(f"Geboortedatum: {geboortedatum}, Voorkeurstijd: {tijd}, Kleur: {kleur}")
        st.write(f"Akkoord? {'Ja' if akkoord else 'Nee'}")

# ----------------------------
# PAGINA: GRAFIEKEN
# ----------------------------
elif sidebar_choice == "Grafieken":
    st.header("📊 Grafieken Demo (zonder Plotly/Matplotlib)")

    # Data maken
    df = pd.DataFrame({
        "x": np.linspace(0, 10, 100),
        "sin(x)": np.sin(np.linspace(0, 10, 100)),
        "cos(x)": np.cos(np.linspace(0, 10, 100))
    }).set_index("x")

    st.subheader("Line chart")
    st.line_chart(df)

    st.subheader("Area chart")
    st.area_chart(df[["sin(x)"]])

    st.subheader("Bar chart")
    st.bar_chart(df.head(20))

# ----------------------------
# PAGINA: DATA
# ----------------------------
elif sidebar_choice == "Data":
    st.header("📑 Data Demo")

    data = {
        "Naam": ["Alice", "Bob", "Charlie", "Diana"],
        "Leeftijd": [24, 30, 22, 28],
        "Stad": ["Amsterdam", "Rotterdam", "Utrecht", "Den Haag"]
    }
    df = pd.DataFrame(data)

    st.subheader("Tabel")
    st.table(df)

    st.subheader("Dataframe")
    st.dataframe(df)

    st.subheader("Kolommen")
    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Temperatuur", "25 °C", "+2 °C")
    col2.metric("💧 Vochtigheid", "55 %", "-5 %")
    col3.metric("⚡ Energie", "120 kWh", "+10 kWh")

# ----------------------------
# PAGINA: WIDGETS
# ----------------------------
elif sidebar_choice == "Widgets":
    st.header("🧰 Widgets Demo")

    st.subheader("Knoppen & inputs")
    if st.button("Klik mij!"):
        st.balloons()

    keuze = st.radio("Kies een optie:", ["🍎 Appel", "🍌 Banaan", "🍒 Kers"])
    st.write("Je koos:", keuze)

    multiselect = st.multiselect(
        "Kies je favoriete talen:", 
        ["Python", "JavaScript", "Rust", "Go"], 
        default=["Python"]
    )
    st.write("Je koos:", multiselect)

    slider = st.slider("Kies een getal:", 0, 100, 50)
    st.write("Je koos:", slider)

    st.subheader("Bestanden uploaden")
    upload = st.file_uploader("Upload een bestand")
    if upload:
        st.write("Bestand geüpload:", upload.name)

    st.subheader("Media")
    st.image("https://placekitten.com/300/200", caption="Een kat 🐱")
    st.audio("https://www2.cs.uic.edu/~i101/SoundFiles/StarWars60.wav")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

