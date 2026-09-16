/*
  Project 1: Plant Monitoring System
  Sensors : Soil Moisture Sensor (Analog) -> A0
            LDR (Light Dependent Resistor)  -> A1
  Sends CSV data over Serial: moisture,light
*/

const int SOIL_PIN = A0;
const int LDR_PIN  = A1;

void setup() {
  Serial.begin(9600);
  pinMode(SOIL_PIN, INPUT);
  pinMode(LDR_PIN, INPUT);
}

void loop() {
  int soilRaw = analogRead(SOIL_PIN);      // 0 (wet) - 1023 (dry) depending on sensor
  int lightRaw = analogRead(LDR_PIN);      // 0 (dark) - 1023 (bright)

  int soilPercent = map(soilRaw, 1023, 0, 0, 100);   // convert to %
  soilPercent = constrain(soilPercent, 0, 100);

  int lightPercent = map(lightRaw, 0, 1023, 0, 100);

  Serial.print(soilPercent);
  Serial.print(",");
  Serial.println(lightPercent);

  delay(1000); // send once per second
}
