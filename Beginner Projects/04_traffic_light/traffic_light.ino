/*
  Project 4: Traffic Light Simulator
  Red LED    -> Pin 8
  Yellow LED -> Pin 9
  Green LED  -> Pin 10

  Serial commands from Python:
    "START" -> begin auto cycling
    "STOP"  -> hold all off
*/

const int RED = 8;
const int YELLOW = 9;
const int GREEN = 10;

bool running = false;
int state = 0; // 0=red,1=green,2=yellow
unsigned long lastChange = 0;
const unsigned long RED_TIME = 4000;
const unsigned long GREEN_TIME = 4000;
const unsigned long YELLOW_TIME = 1500;

void setup() {
  Serial.begin(9600);
  pinMode(RED, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(GREEN, OUTPUT);
  allOff();
}

void allOff() {
  digitalWrite(RED, LOW);
  digitalWrite(YELLOW, LOW);
  digitalWrite(GREEN, LOW);
}

void setLight(int s) {
  allOff();
  if (s == 0) digitalWrite(RED, HIGH);
  else if (s == 1) digitalWrite(GREEN, HIGH);
  else if (s == 2) digitalWrite(YELLOW, HIGH);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "START") {
      running = true;
      state = 0;
      lastChange = millis();
      setLight(state);
    } else if (cmd == "STOP") {
      running = false;
      allOff();
    }
  }

  if (running) {
    unsigned long now = millis();
    unsigned long elapsed = now - lastChange;
    unsigned long duration = (state == 0) ? RED_TIME : (state == 1) ? GREEN_TIME : YELLOW_TIME;

    if (elapsed >= duration) {
      state = (state + 1) % 3;
      lastChange = now;
      setLight(state);
    }
  }

  // Report current state
  static unsigned long lastReport = 0;
  if (millis() - lastReport > 300) {
    lastReport = millis();
    String s = running ? (state == 0 ? "RED" : state == 1 ? "GREEN" : "YELLOW") : "OFF";
    Serial.println(s);
  }
}
