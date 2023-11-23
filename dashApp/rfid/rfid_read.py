from mfrc522 import SimpleMFRC522
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

mqtt_broker_ip = "192.168.74.113"
mqtt_topic_rfid = "RfidData"
reader = SimpleMFRC522()


class RFID(object):
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect(mqtt_broker_ip, 1883, 60)

    try:
        while True:
            print("Hold a tag near the reader")
            id, text = reader.read()
            print("ID: %s\nText: %s" % (id,text))
            
            client.publish(mqtt_topic_rfid, str(id))
            
            time.sleep(1)
    finally:
        print("hello")
