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

st.header('Register Page')
username = st.text_input('Register Username')
st.write('Please scan your RFID card before press button')

if st.button('Register now'):
    curr_data = db.collection('currentUser').document('curr').get().to_dict()
    curr_rfid = curr_data['rfid']


    if username in userList:
        st.warning("The user has been registered", icon='🚨')


    elif (len(username) == 0) or username == 'currentUser':
        st.warning("Invalid username", icon='🚨')


    elif curr_rfid == 'None':
        st.warning("No RFID has been detected (Please scan your card)", icon='🚨')


    else:
        # Register user into database
        # doc_ref_default = db.collection(username).document('userInfo')
        # doc_ref_default.set({
        #     'currPlant': 1,
        #     'distance': 30,
        #     'humidity': 10,
        #     'lightIntensity': 60,
        #     'moisture': 10,
        #     'pH': 7,
        #     'temperature': 28
        # })

        doc_ref_pass = db.collection(username).document('secret')
        doc_ref_pass.set({'password': curr_rfid})
        st.success('Registered Successfully')

        # Set current user
        curr_user = db.collection('currentUser').document('curr')
        curr_user.set({'rfid': 'None', 'user':username})

        # Remove current rfid
        
        switch_page('main')