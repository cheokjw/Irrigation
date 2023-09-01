import streamlit as st
import os
from google.cloud import firestore

# Connect to firestore database by using JSON account key
db = firestore.Client.from_service_account_json("firestore_key.json")

ref = db.collection("plant").document("plantData")

# Obtain data from the collection
doc = ref.get()

# Display obtained data
st.header("Smart Irrigation System")
st.write(f"The id is {doc.id}")
st.write(f"The contents are {doc.to_dict()}")


