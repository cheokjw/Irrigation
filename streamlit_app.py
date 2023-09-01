# Import Necessary Libraries
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
import os
from google.cloud import firestore


# DATABASE ------------------------------------------------
# Connect to firestore database by using JSON account key
db = firestore.Client.from_service_account_json('firestore_key.json')

# Lists out all the collection in the database (For user verification purposes)
userList = [collection.id for collection in db.collections()]

    
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
        st.warning("Username should not be EMPTY!", icon='🚨')
    elif username not in userList:
        st.warning("Username has not been registered", icon='🚨')
    else:
        userInfo = db.collection(username).document('userInfo').to_dict()
        currUser = db.collection('currentUser').document('curr').to_dict()

        if userInfo['rfid'] == currUser['rfid']:
            switch_page('test')
        elif userInfo['rfid'] != currUser['rfid']:
            st.warning("Username and RFID card/tag did not match", icon='🚨')
        else:
            st.warning("Please scan RFID card/ tag", icon='🚨')

# ----------------------------------------------------------


