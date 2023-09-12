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

df = pd.DataFrame({'datetime': ['01-09-2023 15:23:23'], 
                    'distance': [10], 
                    'humidity':[10], 
                    'lightIntensity':[10], 
                    'moisture':[10],
                    'pH': [7], 
                    'temperature':[28]})


for doc in post_ref.stream():
    if doc.id == 'secret':
        break
    data = doc.to_dict()
    temp_df = pd.DataFrame({
        'datetime': [doc.id],
        'distance': [data["distance"]],
        'humidity': [data["humidity"]],
        'lightIntensity': [data["lightIntensity"]],
        'moisture': [data["moisture"]],
        'pH': [data["pH"]],
        'temperature': [data["temperature"]]
    })
    df = pd.concat([df, temp_df], ignore_index = True)

st.dataframe(df)

df['datetime'] = pd.to_datetime(df['datetime'], format='%d-%m-%Y %H:%M:%S')
st.title('Distance Graph')
st.line_chart(data=df[['datetime', 'distance']], x='datetime', y ='distance')

st.title('Humidity Graph')
st.line_chart(data=df[['datetime', 'humidity']], x='datetime', y ='humidity')

st.title('Temperature & Light Intensity Graph')
st.line_chart(data=df[['datetime', 'temperature', 'lightIntensity']], x='datetime', y =['temperature', 'lightIntensity'])

st.title('Humidity Graph')
st.line_chart(data=df[['datetime', 'humidity']], x='datetime', y ='humidity')
# ----------------------------------------------------------


