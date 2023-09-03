import os
import json
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from google.cloud import firestore
from google.oauth2 import service_account
from PIL import Image


# DATABASE ------------------------------------------------
# Connect to firestore database by using JSON account key
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)



# Read all posts 
post_ref = db.collection('currentUser')
# ----------------------------------------------------------



# STREAMLIT ------------------------------------------------


# Page STYLE ===============
st.set_page_config(initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }

    div[role="radiogroup"] >  :first-child{
                display: none !important;
    }
</style>
""",
    unsafe_allow_html=True,
)
# ============================


# Display obtained data
st.header('Smart Irrigation System')

user_choice = 1

# col1, col2, col3 represents the preset plant
col1, col2, col3= st.columns(3)
# First Radio button has been deselected 
with col1:
    if user_choice == 1:
        st.radio(label='Plant 1', options=['One', 'Plant 1'], index=1, label_visibility='collapsed', key='setting1')
    else: 
        st.radio(label='Plant 1', options=['One', 'Plant 1'], label_visibility='collapsed', key='setting1')

    im_plant1 = Image.open('asset/plant1.jpg')
    st.image(im_plant1)
    st.markdown("""
    Distance Threshold    : 30 \n
    Humidity Threshold    : 10 \n
    Light Intensity       : 60 \n
    Moisure Threshold     : 10 \n 
    pH Threshold          : 7  \n
    Temperature Threshold : 28 \n
    """)


with col2:
    if user_choice == 2:
        st.radio(label='Plant 2', options=['One', 'Plant 2'], index=1, label_visibility='collapsed', key='setting2')
    else: 
        st.radio(label='Plant 2', options=['One', 'Plant 2'], label_visibility='collapsed', key='setting2')
    
    im_plant1 = Image.open('asset/plant2.jpg')
    st.image(im_plant1)
    st.markdown("""
    Distance Threshold    : 26 \n
    Humidity Threshold    : 40 \n
    Light Intensity       : 0 \n
    Moisure Threshold     : 10 \n 
    pH Threshold          : 8  \n
    Temperature Threshold : 30 \n
    """)

with col3:
    if user_choice == 3:
        st.radio(label='Plant 3', options=['One', 'Plant 3'],index=1, label_visibility='collapsed', key='setting3')
    else: 
        st.radio(label='Plant 3', options=['One', 'Plant 3'], label_visibility='collapsed', key='setting3')

    im_plant1 = Image.open('asset/plant3.jpg')
    st.image(im_plant1)
    st.markdown("""
    Distance Threshold    : 40 \n
    Humidity Threshold    : 5 \n
    Light Intensity       : 20 \n
    Moisure Threshold     : 40 \n 
    pH Threshold          : 5  \n
    Temperature Threshold : 20 \n
    """)

st.markdown("""---""")

if user_choice == 4:
    st.radio(label='Customize', options=['One', 'Customize'], index=1, label_visibility='collapsed', key='setting4')
else: 
    st.radio(label='Customize', options=['One', 'Customize'], label_visibility='collapsed', key='setting4')

# Check user selection
user_select = [st.session_state.setting1,st.session_state.setting2,st.session_state.setting3,st.session_state.setting4]

st.write(user_select)
