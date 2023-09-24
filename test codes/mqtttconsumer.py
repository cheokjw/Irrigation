import paho.mqtt.client as mqtt

import os
 

plant = 'plant1'

def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(f'paho/IOTtest')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Clearing the Screen
    os.system('cls')
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.subscribe(f'paho/IOTtest')

while True:
    message = client.loop()
    if message:
        print(type(message))