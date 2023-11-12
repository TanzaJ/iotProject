"""
Python MQTT Subscription client - No Username/Password
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
import time

def on_connect(client, usedata, flags, rc):
    if rc == 0:
        print("client is connected")
        global connected
        connected = True
    else:
        print("connection failded")
        
def on_message(client, userdata, message):
    photoData = int(message.payload.decode("utf-8"), 2)
    print(str(message.topic) + ": " + str(photoData))

connected = False
MessageReceived = False
photoData = "0"
port = 1883
mqtt_topic = "LightData"
mqtt_broker_ip = "192.168.0.116"

def getValue():
    return photoData

client = mqtt.Client("Light REader")

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, port=port)

client.loop_start()
client.subscribe(mqtt_topic)
while connected != True:
    time.sleep(0.2)

while MessageReceived != True:
    time.sleep(0.2)
client.loop_stop()

