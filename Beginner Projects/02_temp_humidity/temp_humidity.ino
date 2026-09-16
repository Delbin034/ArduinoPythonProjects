/*
  Project 2: Temperature & Humidity Monitor
  Sensor: DHT11 or DHT22
  Library required: "DHT sensor library" by Adafruit (Install via Library Manager)
  Sends CSV over Serial: temperature,humidity
*/

#include <DHT.h>

#define DHTPIN 2       // DHT data pin
#define DHTTYPE DHT11  // change to DHT22 if using that sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();
  float tempC = dht.readTemperature();

  if (isnan(humidity) || isnan(tempC)) {
    Serial.println("ERR,ERR");
  } else {
    Serial.print(tempC);
    Serial.print(",");
    Serial.println(humidity);
  }

  delay(2000); // DHT11 needs at least 1s between reads
}
