from dash import Dash, dcc, html, Input, Output, State
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Motor1 = 22 # Enable Pin
Motor2 = 27 # Input Pin
Motor3 = 17 # Input Pin
GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)

app = Dash(__name__)

app.layout = html.Div([
    html.Link(rel="stylesheet", href="style.css"),
    html.Link(rel="preconnect", href="https://fonts.googleapis.com"),
    html.Link(rel="preconnect", href="https://fonts.gstatic.com"),
    html.Link(href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,600;0,700;1,300&display=swap", rel="stylesheet"),
    html.Script(src="assets/script.js"),
    html.Script(src="assets/pureknob.js"),

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
            html.P("off", hidden=True, id="fan_state"),
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
    ])
])

@app.callback(
    Output("fan-img", "src"),
    Output("fan-control-button", "children"),
    Output("fan_state", "children"),
    Input("fan-control-button", "n_clicks"),
    State("fan_state", "children"),
    prevent_initial_call=True
)
def toggle_fan(n_clicks, fan_state):
    if fan_state == "off":
        return turnFanOn()
    elif fan_state == "on":
        return turnFanOff()

def turnFanOn():
    GPIO.output(Motor1,GPIO.HIGH)
    GPIO.output(Motor2,GPIO.LOW)
    GPIO.output(Motor3,GPIO.HIGH)
    return app.get_asset_url('images/spinningFan.gif'), "Turn Off", "on"

def turnFanOff():
    GPIO.output(Motor1,GPIO.LOW)
    GPIO.output(Motor2,GPIO.LOW)
    GPIO.output(Motor3,GPIO.LOW)
    return app.get_asset_url('images/spinningFan.png'), "Turn On", "off"

if __name__ == '__main__':
    app.run(debug=True)
