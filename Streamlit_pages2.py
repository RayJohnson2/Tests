import streamlit as st
my_page = st.sidebar.radio('Page Navigation', ['Home', 'Slider', 'Contact'])

if 'slider1' not in st.session_state:
    st.session_state.slider1 = 0
if 'check1' not in st.session_state:
    st.session_state.check1 = False


def CB_Slider1():
    #st.session_state.slider1 = slide1
    pass
    
def home():
    st.write("Welcome to home page")
    st.checkbox("Check me", value=st.session_state.check1, key='check1')
    if st.button("Click Home"):
        st.write("Welcome to home page")


def slider():
    #st.title('this is a different page. One with a slider.')
    st.write("Welcome to the slider page")
    slide1 = st.slider('this is a slider',min_value=0,max_value=15,value=st.session_state.slider1 ,key='slider1' )
    slide1
    


def contact():
    st.title("Welcome to contact page")
    if st.button("Click Contact"):
        st.write("Welcome to contact page")
        
##if my_page == 'page 1':
##    st.title('here is a page')
##    button = st.button('a button')
##    if button:
##        st.write('clicked')
##else:
##    st.title('this is a different page. One with a slider.')
##    slide = st.slider('this is a slider')
##    slide

if my_page == 'Home':
    home()
    
elif my_page == 'Slider':
    slider()
    
elif my_page == 'Contact':
    contact()
    
