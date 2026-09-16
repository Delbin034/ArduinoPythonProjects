/*
  Project 6: Water Level Monitor
  Ultrasonic Sensor HC-SR04
  TRIG -> Pin 9
  ECHO -> Pin 10

  Set TANK_HEIGHT_CM to your actual tank height (distance from sensor
  to bottom of tank when empty).
  Sends: fillPercent
*/

const int TRIG_PIN = 9;
const int ECHO_PIN = 10;
const float TANK_HEIGHT_CM = 100.0; // adjust to your tank

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

float readDistanceCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // 30ms timeout
  float distance = duration * 0.0343 / 2.0;       // speed of sound cm/us
  return distance;
}

void loop() {
  float distance = readDistanceCM();

  float waterHeight = TANK_HEIGHT_CM - distance;
  waterHeight = constrain(waterHeight, 0, TANK_HEIGHT_CM);

  int fillPercent = (int)((waterHeight / TANK_HEIGHT_CM) * 100);

  Serial.println(fillPercent);

  delay(1000);
}
