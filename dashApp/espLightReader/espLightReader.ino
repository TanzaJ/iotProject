#include <ESP8266WiFi.h>
#include <PubSubClient.h>
const char* ssid = "TP-Link_2AD8";
const char* password = "14730078";
//const char* ssid = "TP-LINK_Guest_B043";
//const char* password = "63260588";

const char* mqtt_server = "192.168.0.110";
WiFiClient vanieriot;
PubSubClient client(vanieriot);

const int pResistor = A0; // Photoresistor at Arduino analog pin A0
const int led = D0; // Photoresistor at Arduino analog pin A0
int value;

void setup_wifi() {
   delay(10);
   // We start by connecting to a WiFi network
   Serial.println();
   Serial.print("Connecting to ");
   Serial.println(ssid);
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
   }
   Serial.println("");
   Serial.print("WiFi connected - ESP-8266 IP address: ");
   Serial.println(WiFi.localIP());
}
void callback(String topic, byte* message, unsigned int length) {
   Serial.print("Message arrived on topic: ");
   Serial.print(topic);
   Serial.print(". Message: ");
   String messagein;
  
   for (int i = 0; i < length; i++) {
     Serial.print((char)message[i]);
     messagein += (char)message[i];
   }

}
void reconnect() {
   while (!client.connected()) {
     Serial.print("Attempting MQTT connection...");
     if (client.connect("vanieriot")) {
        Serial.println("connected");
    
     } 
     else {
       Serial.print("failed, rc=");
       Serial.print(client.state());
       Serial.println(" try again in 3 seconds");
       // Wait 5 seconds before retrying
       delay(3000);
     }
   }
}
void setup() {
  Serial.begin(115200);
  pinMode(pResistor, INPUT); // Set pResistor - A0 pin as an input (optional)
  pinMode(led, OUTPUT);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}
void loop() {
  value = analogRead(pResistor);
  String data = String(value, 2);

  Serial.println("Light intensity is: ");
  Serial.println (value);
  client.publish("LightData", data.toCharArray());
  Serial.println ("published");  
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("vanieriot");
  
  delay(5000);
 }
