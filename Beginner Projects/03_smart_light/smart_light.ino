/*
  Project 3: Smart Light Controller
  LDR (Analog) -> A0
  Relay (controls the light/bulb) -> Pin 7

  Modes (settable from Python over Serial):
    "AUTO"  -> relay controlled automatically by light level
    "ON"    -> force relay ON
    "OFF"   -> force relay OFF
*/

const int LDR_PIN = A0;
const int RELAY_PIN = 7;
const int DARK_THRESHOLD = 400; // below this = "dark", turn light ON in AUTO mode

String mode = "AUTO";

void setup() {
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
}

void loop() {
  // Check for incoming mode command
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "AUTO" || cmd == "ON" || cmd == "OFF") {
      mode = cmd;
    }
  }

  int lightRaw = analogRead(LDR_PIN);
  bool relayState;

  if (mode == "ON") {
    relayState = true;
  } else if (mode == "OFF") {
    relayState = false;
  } else { // AUTO
    relayState = (lightRaw < DARK_THRESHOLD);
  }

  digitalWrite(RELAY_PIN, relayState ? HIGH : LOW);

  // Report status: lightLevel,mode,relayState
  Serial.print(lightRaw);
  Serial.print(",");
  Serial.print(mode);
  Serial.print(",");
  Serial.println(relayState ? "ON" : "OFF");

  delay(500);
}
