/*
  Project 8: Weather Station
  DHT11/DHT22   -> Pin 2
  LDR (light)   -> A0
  Rain Sensor (digital, LOW = rain detected on most modules) -> Pin 4

  Library required: "DHT sensor library" by Adafruit
  Sends CSV: temperature,humidity,light,rain
  (rain: 1 = raining, 0 = dry)
*/

#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const int LDR_PIN = A0;
const int RAIN_PIN = 4;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(RAIN_PIN, INPUT);
}

void loop() {
  float tempC = dht.readTemperature();
  float humidity = dht.readHumidity();
  int lightRaw = analogRead(LDR_PIN);
  int lightPercent = map(lightRaw, 0, 1023, 0, 100);
  bool raining = (digitalRead(RAIN_PIN) == LOW);

  if (isnan(tempC) || isnan(humidity)) {
    Serial.println("ERR,ERR,ERR,ERR");
  } else {
    Serial.print(tempC);
    Serial.print(",");
    Serial.print(humidity);
    Serial.print(",");
    Serial.print(lightPercent);
    Serial.print(",");
    Serial.println(raining ? 1 : 0);
  }

  delay(2000);
}
