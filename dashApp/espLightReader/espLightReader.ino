#include <ESP8266WiFi.h>
#include <PubSubClient.h>
const char* ssid = "farouk's phone";
const char* password = "alloallo1";
//const char* ssid = "TP-LINK_Guest_B043";
//const char* password = "63260588";

const char* mqtt_server = "192.168.42.113";
WiFiClient vanieriot;
PubSubClient client(vanieriot);

const int pResistor = A0; // Photoresistor at Arduino analog pin A0
const int led = D0; // Photoresistor at Arduino analog pin A0
int value;

#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN D8
#define RST_PIN D0
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;
// Init array that will store new NUID
byte nuidPICC[4];

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

  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522
  Serial.println();
  Serial.print(F("Reader :"));
  rfid.PCD_DumpVersionToSerial();
  for (byte i = 0; i < 6; i++) {
   key.keyByte[i] = 0xFF;
  }
  Serial.println();
  Serial.println(F("This code scan the MIFARE Classic NUID."));
  Serial.print(F("Using the following key:"));
  printHex(key.keyByte, MFRC522::MF_KEY_SIZE);
}
void loop() {
  String decNUID = "none";
  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
//  if ( ! rfid.PICC_IsNewCardPresent())
//   return;
//  // Verify if the NUID has been readed
//  if ( ! rfid.PICC_ReadCardSerial())
//   return;
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
    // Check is the PICC of Classic MIFARE type
    if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
     piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
     piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
     return;
    }
    if (rfid.uid.uidByte[0] != nuidPICC[0] ||
     rfid.uid.uidByte[1] != nuidPICC[1] ||
     rfid.uid.uidByte[2] != nuidPICC[2] ||
     rfid.uid.uidByte[3] != nuidPICC[3] ) {
     // Store NUID into nuidPICC array
     for (byte i = 0; i < 4; i++) {
      nuidPICC[i] = rfid.uid.uidByte[i];
     }
     decNUID = printDec(rfid.uid.uidByte, rfid.uid.size);
    }
  }
  
  value = analogRead(pResistor);
  char data[4];
  String(value).toCharArray(data, 4);

  char rfidData[decNUID.length() + 1];
  String(decNUID).toCharArray(rfidData, decNUID.length() + 1);

  Serial.println("Light intensity is: ");
  Serial.println (value);
  client.publish("LightData", data);
  Serial.println("RFID NUID is: ");
  Serial.println (decNUID);
  if (decNUID != "none") {   
    client.publish("RfidData", rfidData);
  }
  Serial.println ("published");  
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("vanieriot");
  
  delay(1000);
 }

/**
Helper routine to dump a byte array as hex values to Serial.
*/
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

 /**
 Helper routine to dump a byte array as dec values to Serial.
*/
String printDec(byte *buffer, byte bufferSize) {
  String decNUID = "";
  for (byte i = 0; i < bufferSize; i++) {
   decNUID += buffer[i] < 0x10 ? " 0" : " ";
   decNUID += buffer[i], DEC;
  }
  return decNUID;
}
