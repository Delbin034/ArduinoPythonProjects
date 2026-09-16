/*
  Project 10: Serial Sensor Data Logger
  Generic example: logs 2 analog sensors (change/add as needed)
  Sensor1 -> A0
  Sensor2 -> A1

  Sends CSV: sensor1,sensor2
  (Add more analogRead() lines / Serial.print() calls for more sensors)
*/

const int SENSOR1_PIN = A0;
const int SENSOR2_PIN = A1;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int s1 = analogRead(SENSOR1_PIN);
  int s2 = analogRead(SENSOR2_PIN);

  Serial.print(s1);
  Serial.print(",");
  Serial.println(s2);

  delay(1000);
}
