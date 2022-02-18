import streamlit as st


#my_page = st.sidebar.radio('Page Navigation', ['Home', 'Slider', 'Contact'])

st.session_state.update(st.session_state)

if 'active_page' not in st.session_state:
    st.session_state.active_page = 'Home'
    st.session_state.slider1 = 0
#if 'check1' not in st.session_state:
    st.session_state.check1 = False


def home():
    st.write('Welcome to home page')
    st.checkbox('Check me', key='check1')
    if st.button('Click Home'):
        st.write('Welcome to home page')

def slider():
    #st.title('this is a different page. One with a slider.')
    st.write('Welcome to the slider page')
    slide1 = st.slider('this is a slider',min_value=0,max_value=15,value=st.session_state.slider1 ,key='slider1' )
    slide1
    
def contact():
    st.title('Welcome to contact page')
    if st.button('Click Contact'):
        st.write('Welcome to contact page')
    return

def CB_HomeButton():
    st.session_state.active_page = 'Home'

def CB_SliderButton():
    st.session_state.active_page = 'Slider'

def CB_ContactButton():
    st.session_state.active_page = 'Contact'
    
st.write(f'Multipage app. Streamlit {st.__version__}')
col1, col2, col3 = st.columns(3)

col1.header('Home')
col1.button('Home', on_click=CB_HomeButton)
    
col2.header('Slider demo')
col2.button('Slider', on_click=CB_SliderButton)

col3.header('Contact')
col3.button('Contact', on_click=CB_ContactButton)

st.write('____________________________________________________________________')

if   st.session_state.active_page == 'Home':
    home()
elif st.session_state.active_page == 'Slider':
    slider()
elif st.session_state.active_page == 'Contact':
    contact()

st.write(' ')
st.write(' ')

st.session_state    

    
##if my_page == 'Home':
##    home()
##    
##elif my_page == 'Slider':
##    slider()
##    
##elif my_page == 'Contact':
##    contact()
    
