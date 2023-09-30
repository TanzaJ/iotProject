from flask import Flask, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

led = 17


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)

@app.route('/on')
def on():
    GPIO.output(led, GPIO.HIGH)
    return render_template('on.html')

@app.route('/off')
def off():
    GPIO.output(led, GPIO.LOW)
    return render_template('off.html')
