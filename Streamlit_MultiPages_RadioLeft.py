#-------------------------------------------------------
# Streamlit demo program to handle multiple pages with widget state
# preservation.
# Page selection: radiobuttons on the side bar.
#
# Ray J.
#-------------------------------------------------------

import streamlit as st

#--- I don't understand the necessity of this line. But it is needed
#    to preserve session_state in the cloud. Not locally.
st.session_state.update(st.session_state)

#--- Init session_state
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'Home'
    st.session_state.slider1 = 0
    st.session_state.check1 = False
    st.session_state.radiobuttons = 'Home' 

#--- Payload code of each page
def home():
    st.write('Welcome to home page')
    link = '[GitHub](http://github.com)'
    st.markdown(link, unsafe_allow_html=True)
    st.checkbox('Check me', key='check1')
    if st.button('Click Home'):
        st.write('Welcome to home page')

def slider():
    st.write('Welcome to the slider page')
    slide1 = st.slider('this is a slider',min_value=0,max_value=15,key='slider1' )    
    st.write('Slider position:',slide1)
    
def contact():
    st.title('Welcome to contact page')
    st.write(f'Multipage app. Streamlit {st.__version__}')
    if st.button('Click Contact'):
        st.write('Welcome to contact page')

#--- Callback functions
def CB_RadioButton():
    st.session_state.active_page = st.session_state.radiobuttons

#--- Page selection
st.sidebar.radio('Page Navigation', ['Home', 'Slider', 'Contact'], key='radiobuttons',on_change=CB_RadioButton)
#my_page = st.radio('Page Navigation', ['Home', 'Slider', 'Contact'], key='radiobuttons',on_change=CB_RadioButton)

#--- Run the active page
if   st.session_state.active_page == 'Home':
    home()
elif st.session_state.active_page == 'Slider':
    slider()
elif st.session_state.active_page == 'Contact':
    contact()
 

    
