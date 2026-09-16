/*
  Project 9: Home Appliance Control
  4-Channel Relay Module -> Pins 5, 6, 7, 8
  (LOW-trigger relay boards: LOW = ON, HIGH = OFF. Adjust ACTIVE_LOW if needed.)

  Serial commands from Python: "R1_ON","R1_OFF","R2_ON","R2_OFF", etc.
  Reports state after each change: "R1:ON,R2:OFF,R3:ON,R4:OFF"
*/

const int RELAY_PINS[4] = {5, 6, 7, 8};
bool relayState[4] = {false, false, false, false};
const bool ACTIVE_LOW = true; // most relay boards are active-low

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 4; i++) {
    pinMode(RELAY_PINS[i], OUTPUT);
    writeRelay(i, false);
  }
}

void writeRelay(int index, bool on) {
  relayState[index] = on;
  bool pinVal = ACTIVE_LOW ? !on : on;
  digitalWrite(RELAY_PINS[index], pinVal ? HIGH : LOW);
}

void reportState() {
  for (int i = 0; i < 4; i++) {
    Serial.print("R");
    Serial.print(i + 1);
    Serial.print(":");
    Serial.print(relayState[i] ? "ON" : "OFF");
    if (i < 3) Serial.print(",");
  }
  Serial.println();
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    for (int i = 0; i < 4; i++) {
      String onCmd = "R" + String(i + 1) + "_ON";
      String offCmd = "R" + String(i + 1) + "_OFF";
      if (cmd == onCmd) writeRelay(i, true);
      else if (cmd == offCmd) writeRelay(i, false);
    }
    reportState();
  }
}
