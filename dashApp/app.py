from dash import Dash, dcc, html, Input, Output, State, no_update
import smtplib
import imaplib
import email
from email.header import decode_header
import threading
import Freenove_DHT as DHT
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

List all pins for sensor (James)
sensor_pins = [18, 23, 24]
sensor_data = dict.fromkeys(["temperature", "humidity", "light"], None)

motor_pins = [22, 27, 17]
GPIO.setup(motor_pins[0],GPIO.OUT)
GPIO.setup(motor_pins[1],GPIO.OUT)
GPIO.setup(motor_pins[2],GPIO.OUT)

sender_email = "testvanier@gmail.com"
receiver_email = "testvanier@gmail.com"
password = "hmpz ofwn qxfn byjq"

app = Dash(__name__)

app.layout = html.Div([
    html.Link(rel="stylesheet", href="style.css"),
    html.Link(rel="preconnect", href="https://fonts.googleapis.com"),
    html.Link(rel="preconnect", href="https://fonts.gstatic.com"),
    html.Link(href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,600;0,700;1,300&display=swap", rel="stylesheet"),
    html.Script(src="assets/script.js"),
    html.Script(src="assets/pureknob.js"),
    dcc.Interval(id="readSensorsAndEmailInterval", interval=5000),

    # User preference section
    html.Div(className="container", id="profile", children=[
        html.Div(className="container", id="profileDiv1", children=[
            html.Img(src="assets/images/profilepic.png", id="profilepic")
        ]),
        html.Div(className="container", id="profileDiv2", children=[
            html.H5(style={"font-style": "italic"}, children="Welcome"),
            html.H1(style={"font-size": "42pt"}, children="<Username>")
        ]),
        html.Div(className="container", id="profileDiv3", children=[
            html.H5(style={"font-weight": "600"}, children="Saturday, October 7, 2023"),
            html.H1(style={"font-size": "48pt"}, children="12:12PM")
        ]),
        html.Div(className="container", id="profileDiv4", children=[
            html.H5(style={"font-style": "italic"}, children="Preferences"),
            html.Form(action="", id="preferencesForm", children=[
                html.Label(htmlFor="", children=[
                    html.H5("Temperature")
                ]),
                html.Div(children=[
                    dcc.Input(type="text", maxLength="3", value="27"),
                    '\N{DEGREE SIGN}' + "C"
                ]),

                html.Label(htmlFor="", children=[
                    html.H5("Humidity")
                ]),
                html.Div(children=[
                    dcc.Input(type="text", maxLength="3", value="70"),
                    "%"
                ]),

                html.Label(htmlFor="", children=[
                    html.H5("Light Intensity")
                ]),
                html.Div(children=[
                    dcc.Input(type="text", maxLength="3", value="505")
                ]),

                html.Button(id="savePrefsBtn", n_clicks=0, children="Save Preferences")
            ])
        ]),
    ]),
    # Temperature section
    html.Div(className="container", id="tempHumFan", children=[
        html.Div(className="container", id="tempContainer", children=[
            html.Div(className="container", id="thermometerGauge"),
            html.H2("Current Temperature")
        ]),
        html.Div(className="container", id="humidity", children=[
            html.Div(className="container", id="humidityGauge"),
            html.H2("Current Humidity", style={"color": "#76c8e3"})
        ]),
        html.Div(className="container", id="fan", children=[
            html.P("fanOff", hidden=True, id="fan_state"),
            html.Img(src=app.get_asset_url("images/spinningFan.png"), id="fan-img", width="250", height="250"),
            html.Button("Turn On", id="fan-control-button", n_clicks=0)
        ])
    ]),

    # Light section
    html.Div(className="container", id="light", children=[
        html.Img(src="assets/images/phase1On.png", id="lightImg"),
        html.Div(id="lightText", children=[
            html.H2("Current Light Intensity"),
            html.H2("495", style={"color": "#FFCA10"})
        ])
    ]),

    # Devices section
    html.Div(className="container", id="devices", children=[
        html.Img(src="assets/images/phone.png", id="devicesImg"),
        html.Div(id="devicesText", children=[
            html.H2("Wireless Devices Nearby"),
            html.H2("7")
        ])
    ]),
    html.Button("Send Test Email", id="send-email-button"),
    html.Div(id="email-status")
])


@app.callback(
    Output("fan_state", "children", allow_duplicate=True),
    Input("readSensorsAndEmailInterval", "n_intervals"),
    prevent_initial_call=True
)
def sensor_and_email_reader(n_intervals):
    global sensor_data
    
    print("Measurement counts: ", n_intervals)
    dhtReading(sensor_pins[0])
    user_response = check_email_for_user_response()
    if user_response == "fanOn":
        return user_response
    return no_update

@app.callback(
    Output("fan_state", "children"),
    Input("fan-control-button", "n_clicks"),
    State("fan_state", "children"),
    prevent_initial_call=True
)
def toggle_fanState(n_clicks, fan_state):
    if fan_state == "fanOff":
        return "fanOn"
    elif fan_state == "fanOn":
        return "fanOff"

@app.callback(
    Output("fan-img", "src"),
    Output("fan-control-button", "children"),
    Input("fan_state", "children"),
    prevent_initial_call=True
)
def update_fan(fan_state):
    if fan_state == "fanOff":
        return turnFanOff()
    elif fan_state == "fanOn":
        return turnFanOn()

def turnFanOn():
    GPIO.output(motor_pins[0],GPIO.HIGH)
    GPIO.output(motor_pins[1],GPIO.LOW)
    GPIO.output(motor_pins[2],GPIO.HIGH)
    return app.get_asset_url('images/spinningFan.gif'), "Turn Off"

def turnFanOff():
    GPIO.output(motor_pins[0],GPIO.LOW)
    GPIO.output(motor_pins[1],GPIO.LOW)
    GPIO.output(motor_pins[2],GPIO.LOW)
    return app.get_asset_url('images/spinningFan.png'), "Turn On"

#email sending and receiving logic:

@app.callback(
    Output("email-status", "children"),
    Input("send-email-button", "n_clicks"),
    prevent_initial_call=True
)

def send_test_email(n_clicks):
    # Manually send a test email
    subject = "Test Email"
    body = "This is a test email. Please reply to this email 'YES' to turn on the fan."
    send_email(subject, body)
    return "Test email sent."

def send_email(subject, body):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully.")
    except Exception as e:
        print("Email could not be sent. Error:", str(e))

def check_email_for_user_response():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(sender_email, password)
        mail.select("inbox")
        status, email_ids = mail.search(None, "UNSEEN")

        email_ids = email_ids[0].split()

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]

            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            print("From:", msg["From"])
            print("Subject:", subject)
            print("Date:", msg["Date"])

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        email_body = part.get_payload(decode=True).decode("utf-8")
                        print("Email Body:", email_body)

                        first_word = email_body.strip().split()[0]

                        if first_word.upper() == "YES":
                            print("Received 'YES' response. Turning on the fan...")
                            return "fanOn"
                        else:
                            print("No 'YES' found in the email body.")
        mail.logout()
    except Exception as e:
        print("Email retrieval error:", str(e))


#Sensor Functions: (James)

# (James)
            
#DHT (James)
def dhtReading(sensor_index):
    dht = DHT.DHT(sensor_index) #create a DHT class object
    
    # for i in range(0,15):
    #     chk = dht.readDHT11()
    #     if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine
    #         print("DHT11,OK!")
    #         break
    #     sleep(0.1)
    sensor_data['temperature'] = dht.temperature
    sensor_data['humidity'] = dht.humidity
    print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))

if __name__ == '__main__':
    #threading.Thread(target=sensorandemail_reader).start()
    app.run(debug=True)
