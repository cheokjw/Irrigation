import os
import json
import time
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from google.cloud import firestore
from google.oauth2 import service_account
from PIL import Image


# DATABASE ------------------------------------------------
# Connect to firestore database by using JSON account key
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)



# Read current user collection
post_ref = db.collection('currentUser')

# Get current user
currData = db.collection('currentUser').document('curr').get().to_dict()

# Set current user
user = currData['user']

current_user_ref =  db.collection('currentUser').document('curr').get().to_dict()
post_ref2 = db.collection(current_user_ref['user'])
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
if st.button('BACK TO HOME PAGE 👈'):
    switch_page('main')
    
st.header('Plant SETTINGS 🛞')

mac_add = st.text_input('Enter MAC Address of your device')
mac_ref = ''

# Test
if st.button('Plant 1🪴'):
    st.write('test')
    post_ref2.document(mac_add).set({
        'currPlant': 1,
        'distance': 30,
        'humidity': 10,
        'lightIntensity': 60,
        'moisture': 10,
        'pH': 7,
        'temperature': 28
    })

im_plant1 = Image.open('asset/plant1.jpg')
st.image(im_plant1)
st.markdown("""
Distance Threshold    : 30 \n
Humidity Threshold    : 10 \n
Light Intensity       : 60 \n
Moisure Threshold     : 10 \n 
pH Threshold          : 7  \n
Temperature Threshold : 28 \n
""")

# ----
if st.button('Submit'):
    if len(mac_add) == 0:
        st.warning('Please enter MAC Adress of your device', icon='🚨')
    elif mac_add not in [mac.id for mac in post_ref2.stream()]:
        st.warning('MAC Address does not exist in database', icon='🚨')
    else:
        userData = post_ref2.document(mac_add).get().to_dict()
        currPlant = userData['currPlant']
        plantText = ''
        if currPlant == 1:
            plantText = 'Plant 1'
        elif currPlant == 2:
            plantText = 'Plant 2'
        elif currPlant == 3:
            plantText = 'Plant 3'
        elif currPlant == 4:
            plantText = 'Customized Plant'
        else:
            plantText = 'No Plant Selected'

        st.write(f'Your current setting : {plantText}\n\n')

        # col1, col2, col3 represents the preset plant
        col1, col2, col3= st.columns(3)

        with col1:
            im_plant1 = Image.open('asset/plant1.jpg')
            st.image(im_plant1)
            st.markdown("""
            Distance Threshold    : 30 \n
            Humidity Threshold    : 10 \n
            Light Intensity       : 60 \n
            Moisure Threshold     : 10 \n 
            pH Threshold          : 7  \n
            Temperature Threshold : 28 \n
            """)
            if st.button('Plant 1🪴'):
                st.write('test')
                post_ref2.document(mac_add).set({
                    'currPlant': 1,
                    'distance': 30,
                    'humidity': 10,
                    'lightIntensity': 60,
                    'moisture': 10,
                    'pH': 7,
                    'temperature': 28
                })



        with col2:
            
            im_plant1 = Image.open('asset/plant2.jpg')
            st.image(im_plant1)
            st.markdown("""
            Distance Threshold    : 26 \n
            Humidity Threshold    : 40 \n
            Light Intensity       : 0 \n
            Moisure Threshold     : 10 \n 
            pH Threshold          : 8  \n
            Temperature Threshold : 30 \n
            """)
            if st.button('Plant 2🪴'):
                plantText = 'Plant 2'
                post_ref2.document(mac_add).set({
                    'currPlant': 2,
                    'distance': 26,
                    'humidity': 40,
                    'lightIntensity': 0,
                    'moisture': 10,
                    'pH': 8,
                    'temperature': 30
                })

        with col3:

            im_plant1 = Image.open('asset/plant3.jpg')
            st.image(im_plant1)
            st.markdown("""
            Distance Threshold    : 40 \n
            Humidity Threshold    : 5 \n
            Light Intensity       : 20 \n
            Moisure Threshold     : 40 \n 
            pH Threshold          : 5  \n
            Temperature Threshold : 20 \n
            """)
            if st.button('Plant 3🪴'):
                plantText = 'Plant 3'
                post_ref2.document(mac_add).set({
                    'currPlant': 3,
                    'distance': 40,
                    'humidity': 5,
                    'lightIntensity': 20,
                    'moisture': 40,
                    'pH': 5,
                    'temperature': 20
                })

        st.markdown("""---""")

        # Customizable plant
        st.header('Customize Plant Settings')

        distance = st.slider('Distance', 0, 500, userData['distance'])
        humidity = st.slider('Humidity', 0, 100, userData['humidity'])
        light = st.slider('Light Intensity', 0, 100, userData['lightIntensity'])
        moisture = st.slider('Moisture Level', 0, 100, userData['moisture'])
        ph = st.slider('pH Level', 0, 14, userData['pH'])
        temp = st.slider('Temperature', 0, 50, userData['temperature'])



        if st.button('Customize 🪴'):
            plantText = 'Customized Plant'
            post_ref2.document(mac_add).set({
                'currPlant': 4,
                'distance': distance,
                'humidity': humidity,
                'lightIntensity': light,
                'moisture': moisture,
                'pH': ph,
                'temperature': temp
            })

