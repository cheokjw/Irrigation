import os
import json
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from google.cloud import firestore
from google.oauth2 import service_account


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

user_choice = 2

# col1, col2, col3 represents the preset plant
# col4 represents the user modified plant settings
col1, col2, col3, col4 = st.columns(4)


# First Radio button has been deselected 
with col1:
    if user_choice == 1:
        st.radio(label='Plant 1', options=['One', 'Plant 1'], index=1, label_visibility='collapsed')
    else: 
        st.radio(label='Plant 1', options=['One', 'Plant 1'], label_visibility='collapsed')


with col2:
    if user_choice == 2:
        st.radio(label='Plant 2', options=['One', 'Plant 2'], index=1, label_visibility='collapsed')
    else: 
        st.radio(label='Plant 2', options=['One', 'Plant 2'], label_visibility='collapsed')

with col3:
    if user_choice == 3:
        st.radio(label='Plant 3', options=['One', 'Plant 3'],index=1, label_visibility='collapsed')
    else: 
        st.radio(label='Plant 3', options=['One', 'Plant 3'], label_visibility='collapsed')

with col4:
    if user_choice == 3:
        st.radio(label='Customize', options=['One', 'Customize'], index=1, label_visibility='collapsed')
    else: 
        st.radio(label='Customize', options=['One', 'Customize'], label_visibility='collapsed')