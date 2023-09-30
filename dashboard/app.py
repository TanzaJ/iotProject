from flask import Flask
from flask_socketio import SocketIO, emit
import threading
import random
import time
import RPi.GPIO as GPIO

app = Flask(__name__)
socketio = SocketIO(app)

# Assume we have 3 sensors
sensor_data = [None, None, None]

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
motor_pins = [17, 22, 27]
sensor_pins = [ 18, 23, 24]

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
        if socketio.connections:
            sensor_data[sensor_index] = read_sensor_data(sensor_index)
            socketio.emit('sensor_data', {'sensor_index': sensor_index, 'data': sensor_data[sensor_index]})

@socketio.on('connect')
def handle_connect(host_connection):
    print('Successfully connected to: ' + host_connection)
    socket.send('Connected to server!')
        
@socketio.on('message')
def handle_message(data):
    print('Received message: ' + data)

@socketio.on('disconnect')
def handle_connect(host_connection):
    print('Connection Lost: ' + host_connection)
    socket.send('Disconnected from server!')
    
if __name__ == '__main__':
    for i in len(sensor_pins):
        threading.Thread(target=sensor_reader, args=(i,)).start()
    socketio.run(app, host='0.0.0.0', port=5000)