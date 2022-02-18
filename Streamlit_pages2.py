import streamlit as st

my_page = st.sidebar.radio('Page Navigation', ['Home', 'Slider', 'Contact'])

st.session_state.update(st.session_state)

if 'slider1' not in st.session_state:
    st.session_state.slider1 = 0
if 'check1' not in st.session_state:
    st.session_state.check1 = False

def home():
    st.write("Welcome to home page")
    st.session_state
    st.checkbox("Check me", key='check1')
    if st.button("Click Home"):
        st.write("Welcome to home page")

def slider():
    #st.title('this is a different page. One with a slider.')
    st.write("Welcome to the slider page")
    st.session_state
    slide1 = st.slider('this is a slider',min_value=0,max_value=15,value=st.session_state.slider1 ,key='slider1' )
    slide1
    
def contact():
    st.title("Welcome to contact page")
    st.session_state
    if st.button("Click Contact"):
        st.write("Welcome to contact page")

if my_page == 'Home':
    home()
    
elif my_page == 'Slider':
    slider()
    
elif my_page == 'Contact':
    contact()
    
