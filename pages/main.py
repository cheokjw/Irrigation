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
import time

now = datetime.now()
curr = now.strftime("%d-%m-%Y %H:%M:%S")
print(curr)

# DATABASE ------------------------------------------------
# Connect to firestore database by using JSON account key
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)



# Read all posts 
current_user_ref =  db.collection('currentUser').document('curr').get().to_dict()
post_ref = db.collection(current_user_ref['user'])
# ----------------------------------------------------------


# MQTT -----------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # st.write("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('paho/IOTtest/#')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
    if msg.topic == f'paho/IOTtest/{mac_add}/humidity':
        hum_container.text("Humidity: " + str(msg.payload)[2:-1])
    if msg.topic == f'paho/IOTtest/{mac_add}/lightIntensity':
        light_container.text("Light: " + str(msg.payload)[2:-1])
    if msg.topic == f'paho/IOTtest/{mac_add}/moisture':
        moisture_container.text("Moisture: " + str(msg.payload)[2:-1])
    if msg.topic == f'paho/IOTtest/{mac_add}/temperature':
        temperature_container.text("Temperature: " + str(msg.payload)[2:-1])
    if msg.topic == f'paho/IOTtest/{mac_add}/status':
        sensor1_container.text("Status: " + str(msg.payload)[2:-1])
    if msg.topic == f'paho/IOTtest/{mac_add}/water':
        sensor2_container.text("Water: " + str(msg.payload)[2:-1])


# Connect to MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.subscribe('paho/IOTtest/#')
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

col1, col2 = st.columns(2)

with col1:
    if st.button('🛞'):
        switch_page('settings')

with col2:
    if st.button('Logout❗'):
        curr_user = db.collection('currentUser').document('curr')
        curr_user.set({'rfid': "b''", 'user': 'None'})
        switch_page('streamlit_app')

# Ask user to enter MAC address
mac_add = st.text_input('Enter MAC Address of your device')
mac_ref = ''

st.write("Remember to refresh the page after adding sensors")
# List out all of current devices
device_list = [doc.id for doc in post_ref.list_documents() if doc.id != 'secret']
string = ''
st.write(device_list)

st.header('Real Time Data')
con1, con2, con3, con4 = st.columns(4)
with con1:
    hum_container = st.empty()
with con2:
    light_container = st.empty()
with con3:
    moisture_container = st.empty()
with con4:
    temperature_container = st.empty()

st.header('Sensor Status')
sensor1_container = st.empty()
sensor2_container = st.empty()
st.markdown(
    """
    ---
    """
)

if st.button('Submit'):
    # creating a single-element container
    placeholder = st.empty()
    current_user_ref =  db.collection('currentUser').document('curr').get().to_dict()
    post_ref = db.collection(current_user_ref['user'])
    if len(mac_add) == 0:
        st.warning('Please enter MAC Adress of your device', icon='🚨')
    elif mac_add not in [mac.id for mac in post_ref.stream()]:
        st.warning('MAC Address does not exist in database', icon='🚨')
    else:
        while True:
            # MQTT Part ----------------------------------------------------------
            message = client.loop()
            # Historical Data Part -----------------------------------------------
            mac_ref = post_ref.document(mac_add).collection('data')
            df = pd.DataFrame({'datetime': ['12-09-2023 15:23:23'], 
                        'humidity':['10'], 
                        'lightIntensity':['10'], 
                        'moisture':['10'],
                        'temperature':['28']})

            for doc in mac_ref.stream():
                data = doc.to_dict()
                temp_df = pd.DataFrame({
                    'datetime': [doc.id],
                    'humidity': [data["humidity"]],
                    'lightIntensity': [data["lightIntensity"]],
                    'moisture': [data["moisture"]],
                    'temperature': [data["temperature"]]
                })
                df = pd.concat([df, temp_df], ignore_index = True)  

            with placeholder.container():
                st.dataframe(df.tail(5))

                # Convert DataType
                df['datetime'] = pd.to_datetime(df['datetime'], format='%d-%m-%Y %H:%M:%S')
                df["humidity"] = df["humidity"].astype(float)
                df["lightIntensity"] = df["lightIntensity"].astype(float)
                df["moisture"] = df["moisture"].astype(float)
                df["temperature"] = df["temperature"].astype(float)

                # Display Graphs
                st.title('Humidity Graph')
                st.line_chart(data=df[['datetime', 'humidity']], x='datetime', y ='humidity')

                st.title('Moisture Graph')
                st.line_chart(data=df[['datetime', 'moisture']], x='datetime', y ='moisture')

                st.title('Temperature Graph')
                st.area_chart(data=df[['datetime', 'temperature']], x='datetime', y ='temperature')

                st.title('Light Intensity Graph')
                st.line_chart(data=df[['datetime', 'lightIntensity']], x='datetime', y ='lightIntensity')
                time.sleep(1)

            # ----------------------------------------------------------




