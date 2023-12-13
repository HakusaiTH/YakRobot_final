#include <FirebaseESP8266.h>

#if defined(ESP32)
#include <WiFi.h>
#elif defined(ESP8266)
#include <ESP8266WiFi.h>
#endif

#define WIFI_SSID "" // your wifi SSID
#define WIFI_PASSWORD "" // your wifi PASSWORD

#define FIREBASE_HOST "... firebasedatabase.app"
#define FIREBASE_AUTH "" // your private key

FirebaseData firebaseData;

const int RelayPin = D1; // Change to the pin connected to your relay

void setup()
{
  Serial.begin(9600);

  // Connect to WiFi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected: ");
  Serial.println(WiFi.localIP());

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  pinMode(RelayPin, OUTPUT);
  digitalWrite(RelayPin, HIGH);
}

void loop()
{
  if (Firebase.getString(firebaseData, "/room/A1/led_1"))
  {
    String ledStatus = firebaseData.stringData();
    Serial.println(ledStatus);

    if (ledStatus == "ON")
    {
      digitalWrite(RelayPin, LOW); // Relay ON
    }
    else if (ledStatus == "OFF")
    {
      digitalWrite(RelayPin, HIGH); // Relay OFF
    }
    else
    {
      Serial.println("Invalid LED status received from Firebase");
    }
  }
  else
  {
    Serial.print("Error: ");
    Serial.println(firebaseData.errorReason());
  }

  delay(1000); // Adjust the delay as needed
}
