# Import Necessary Libraries
import streamlit as st
from datetime import datetime
import os
from google.cloud import firestore


# DATABASE ------------------------------------------------
# Connect to firestore database by using JSON account key
db = firestore.Client.from_service_account_json('firestore_key.json')

# Lists out all the collection in the database (For user verification purposes)
collections = [collection.id for collection in db.collections()]

    
# Read all posts 
post_ref = db.collection('user1')
# ----------------------------------------------------------


# STREAMLIT FUNCTIONS --------------------------------------
# ----------------------------------------------------------


# STREAMLIT ------------------------------------------------

# Page STYLE ===============
# st.set_page_config(initial_sidebar_state="collapsed")
# st.markdown(
#     """
# <style>
#     [data-testid="collapsedControl"] {
#         display: none
#     }
# </style>
# """,
#     unsafe_allow_html=True,
# )
# ============================


# Display obtained data
st.header('Smart Irrigation System')

username = st.text_input('Username: ')

if st.button('Login'):
    if len(username) == 0:
        st.toast("Username field should not be EMPTY!", icon='🚨')
# ----------------------------------------------------------


