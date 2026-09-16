/*
  Project 7: Flame Detection System
  Flame Sensor (Digital output) -> Pin 2   (LOW = flame detected on most modules)
  Buzzer                        -> Pin 8
  Sends: "FIRE" or "SAFE"
*/

const int FLAME_PIN = 2;
const int BUZZER_PIN = 8;

void setup() {
  Serial.begin(9600);
  pinMode(FLAME_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
}

void loop() {
  int flameState = digitalRead(FLAME_PIN);
  bool fireDetected = (flameState == LOW); // most flame sensor modules pull LOW on detection

  digitalWrite(BUZZER_PIN, fireDetected ? HIGH : LOW);

  Serial.println(fireDetected ? "FIRE" : "SAFE");

  delay(300);
}
