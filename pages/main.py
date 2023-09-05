# Import Necessary Libraries
from datetime import datetime
import os
import json
import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from google.cloud import firestore
from google.oauth2 import service_account

now = datetime.now()
curr = now.strftime("%d-%m-%Y %H:%M:%S")
print(curr)

# DATABASE ------------------------------------------------
# Connect to firestore database by using JSON account key
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

# TODO: ADD LOGOUT BUTTON, SUBSCRIBE MQTT

# # Write Sample data into firestore
# doc_ref = db.collection('user1').document(str(curr))
# doc_ref.set({
#     'distance': 40,
#     'humidity': 10,
#     'lightIntensity': 60,
#     'moisture': 10,
#     'pH': 7,
#     'temperature': 28
# })


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


# Display obtained data
st.header('Smart Irrigation System')

if st.button('🛞'):
    switch_page('settings')

df = pd.DataFrame(columns=['datetime', 'distance', 'humidity', 'lightIntensity', 'moisture', 'pH', 'temperature'])

for doc in post_ref.stream():
    data = doc.to_dict()
    temp_df = pd.DataFrame({
        'datetime': doc.id,
        'distance': data['distance'],
        'humidity': data['humidity'],
        'lightIntensity': data['lightIntensity'],
        'moisture': data['moisture'],
        'pH': data['pH'],
        'temperature': data['temperature']
    })
    df.append(temp_df)

st.dataframe(df)

# ----------------------------------------------------------


