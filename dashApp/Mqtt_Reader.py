"""
Python MQTT Subscription client - No Username/Password
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
import time

def on_connect(client, usedata, flags, rc):
    if rc == 0:
        global connected
        connected = True
    # else:
        # print("connection failded")
        
def on_message(client, userdata, message):
    global photoData
    photoData = int(message.payload.decode("utf-8"))
    global messageReceived
    messageReceived = True
    # print(str(message.topic) + ": " + str(photoData))

def getValue():
    global connected
    connected = False
    global messageReceived
    messageReceived = False
    port = 1883
    mqtt_topic = "LightData"
    mqtt_broker_ip = "192.168.58.113"

    client = mqtt.Client("Light REader")

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker_ip, port=port)

    client.loop_start()
    client.subscribe(mqtt_topic)
    while connected != True:
        time.sleep(0.2)

    while messageReceived != True:
        time.sleep(0.2)
    client.loop_stop()
    client.loop_stop()

    global photoData
    return photoData

