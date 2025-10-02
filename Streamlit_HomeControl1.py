#-------------------------------------------------------
# Streamlit demo program to handle multiple pages with widget state
# preservation.
# Page selection: radiobuttons on the side bar.
#
# Ray J.
#-------------------------------------------------------

import streamlit as st
st.button("Click me")
data = ''
st.download_button("Download file", data)
url = 'www.google.com'
st.link_button("Go to gallery", url)

# st.page_link("app.py", label="Home")
# st.data_editor("Edit data", data)
st.checkbox("I agree")
st.feedback("thumbs")
st.pills("Tags", ["Sports", "Politics", "S*x", "Drugs", "Rock and roll"])
st.radio("Pick one", ["cats", "dogs","sharks","Even worse"])
st.segmented_control("Filter", ["Open", "Closed","more closed","completely shut"])
st.toggle("Enable")
st.selectbox("Pick one", ["cats", "dogs","sharks","Even worse"])
st.multiselect("Buy", ["milk", "apples", "potatoes","Open", "Closed","more closed","completely shut"])
st.slider("Pick a number", 0, 100)
st.select_slider("Pick a size", ["S", "M", "L"])
st.text_input("First name")
st.number_input("Pick a number", 0, 10)
st.text_area("Text to translate")
st.date_input("Your birthday")
st.time_input("Meeting time")
st.file_uploader("Upload a CSV")
st.audio_input("Record a voice message")
st.camera_input("Take a picture")
st.color_picker("Pick a color")




