# Import Necessary Libraries ------------------------------
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
import os
import json
from google.cloud import firestore
from google.oauth2 import service_account
# ---------------------------------------------------------

# DATABASE ------------------------------------------------
# Connect to firestore database by using JSON account key
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

# Lists out all the collection in the database (For user verification purposes)
userList = [collection.id for collection in db.collections()]

    
# Read all posts 
post_ref = db.collection('user1')
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
</style>
""",
    unsafe_allow_html=True,
)
# ============================


# Display Page
st.header('Smart Irrigation System')

# LOGIN FUNCTION ===================================================================
username = st.text_input('Username: ')

if st.button('Login'):

    if len(username) == 0:
        st.warning("Username should not be EMPTY!", icon='🚨')

    elif username not in userList:
        st.warning("Username has not been registered", icon='🚨')
    else:
        userInfo = db.collection(username).document('secret').get().to_dict()
        currUser = db.collection('currentUser').document('curr').get().to_dict()

        if userInfo['password'] == currUser['rfid']:
            curr_username = db.collection('currentUser').document('curr')
            curr_username.set({'rfid': "b''", 'user':username})
            switch_page('main')

        elif userInfo['password'] != currUser['rfid']:
            st.warning("Username and RFID card/tag did not match", icon='🚨')
        else:
            st.warning("Please scan RFID card/ tag", icon='🚨')

elif st.button('Don\'t have an account yet? Click to Register'):
    switch_page('register')
# =================================================================================

# ----------------------------------------------------------


