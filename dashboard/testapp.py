#from flask import Flask, render_template, send_from_directory, request
#from flask_socketio import SocketIO, emit
from dash import Dash, dcc, html
import plotly.express as px
import threading
import random
import Freenove_DHT as DHT
import RPi.GPIO as GPIO
from time import sleep

app = Dash(__name__)

connected_users = {}
sensor_data = [None, None, None]

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
motor_pins = [17, 22, 27]
sensor_pins = [18, 23, 24]

# Setup sensor pins
for pin in sensor_pins:
    GPIO.setup(pin, GPIO.IN)

# Setup motor pins
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

def run_motor():
    GPIO.output(motor_pins[0],GPIO.HIGH)
    GPIO.output(motor_pins[1],GPIO.LOW)
    GPIO.output(motor_pins[2],GPIO.HIGH)

def read_sensor_data(sensor_index):
    # Read data from GPIO
    return GPIO.input(sensor_pins[sensor_index])

def sensor_reader(sensor_index):
    global sensor_data
    while True:
        if len(connected_users) != 0:
            if sensor_index == sensor_pins[0]:
                dhtLoop(sensor_index)
            # sensor_data[sensor_index] = read_sensor_data(sensor_index)
            # socketio.emit('sensor_data', {'sensor_index': sensor_index, 'data': sensor_data[sensor_index]}


if __name__ == '__main__':
#    for i in sensor_pins:
#        threading.Thread(target= sensor_reader, args=(i,)).start()
    app.run(debug=True)


    
def dhtLoop(sensor_index):
    dht = DHT.DHT(sensor_index) #create a DHT class object
    
    counts = 0 # Measurement counts
    while(True):
        counts += 1
        print("Measurement counts: ", counts)
        for i in range(0,15):
            chk = dht.readDHT11()
            if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine
                print("DHT11,OK!")
                break
            sleep(0.1)
        print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
        socketio.emit('sensor_data', {'sensor_type': 'temp', 'data': dht.temperature})
        socketio.emit('sensor_data', {'sensor_type': 'humidity', 'data': dht.humidity})
        sleep(2)
