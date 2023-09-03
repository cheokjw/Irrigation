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

# col1, col2, col3 represents the preset plant
# col4 represents the user modified plant settings
col1, col2, col3, col4 = st.columns(4)


# First Radio button has been deselected 
with col1:
    st.radio(label='test', options=['One', 'Two'])

with col2:
    st.radio(label='test1', options=['One2', 'Two2'])

with col3:
    st.radio(label='test2', options=['One3', 'Two3'])

with col4:
    st.radio(label='test3', options=['One4', 'Two4'])