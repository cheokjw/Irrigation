# Import Necessary Libraries
import streamlit as st
from datetime import datetime
import os
from google.cloud import firestore

now = datetime.now()
curr = now.strftime("%d/%m/%Y %H:%M:%S")

# DATABASE ------------------------------------------------
# Connect to firestore database by using JSON account key
db = firestore.Client.from_service_account_json('firestore_key.json')


# Write Sample data into firestore
doc_ref = db.collection('plant').document(curr)
doc_ref.set({
    'distance': 12,
    'humidity': 30,
    'lightIntensity': 50,
    'moisture': 20,
    'pH': 5,
    'temperature': 28
})


# Read all posts (Change to 'user' in the future)
posts_ref = db.collection('plant')
# ----------------------------------------------------------



# STREAMLIT ------------------------------------------------
# Display obtained data
st.header('Smart Irrigation System')

for doc in post_ref.stream():
    st.write(f'The id is: {doc.id}')
    st.write(f'The contents are: ', doc.to_dict())

# ----------------------------------------------------------


