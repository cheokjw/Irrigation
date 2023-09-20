# Import Necessary Libraries
from datetime import datetime
import os
import json
import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from google.cloud import firestore
from google.oauth2 import service_account
import paho.mqtt.client as mqtt
import threading
import queue



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
current_user_ref =  db.collection('currentUser').document('curr').get().to_dict()
post_ref = db.collection(current_user_ref['user'])
# ----------------------------------------------------------


# MQTT -----------------------------------------------------

q = queue.Queue()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    q.put(str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('paho/IOTtest')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    q.put(msg.payload)
    print(msg.topic+" "+str(msg.payload))

# Connect to MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)


def mqtt_thread():
    client.subscribe('paho/IOTtest')
    client.loop_start()


thread = None
running = True
thread = threading.Thread(target=mqtt_thread)
thread.start()
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

# Ask user to enter MAC address
mac_add = st.text_input('Enter MAC Address of your device')
mac_ref = ''
if st.button('Submit'):
    if len(mac_add) == 0:
        st.warning('Please enter MAC Adress of your device', icon='🚨')
    elif mac_add not in [mac.id for mac in post_ref.stream()]:
        st.warning('MAC Address does not exist in database', icon='🚨')
    else:
        mac_ref = post_ref.document(mac_add).collection('data')
        df = pd.DataFrame({'datetime': ['2023-09-12 15:23:23'], 
                    'distance': [10], 
                    'humidity':[10], 
                    'lightIntensity':[10], 
                    'moisture':[10],
                    'pH': [7], 
                    'temperature':[28]})

        for doc in mac_ref.stream():
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

        df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')
        st.title('Distance Graph')
        st.line_chart(data=df[['datetime', 'distance']], x='datetime', y ='distance')

        st.title('Humidity & Moisture Graph')
        st.line_chart(data=df[['datetime', 'humidity', 'moisture']], x='datetime', y =['humidity', 'moisture'])

        st.title('Temperature & Light Intensity Graph')
        st.area_chart(data=df[['datetime', 'temperature', 'lightIntensity']], x='datetime', y =['temperature', 'lightIntensity'])

        st.title('pH Graph')
        st.line_chart(data=df[['datetime', 'pH']], x='datetime', y ='pH')
        # ----------------------------------------------------------




