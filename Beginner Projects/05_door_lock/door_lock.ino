/*
  Project 5: Arduino Digital Door Lock
  4x4 Keypad + Servo motor lock
  Library required: "Keypad" by Mark Stanley (Install via Library Manager)
                     "Servo" (built-in)

  Password can be changed live from Python over Serial with command:
    "SETPASS:1234"
  Serial reports: "UNLOCKED" or "DENIED" or "PASS_SET"
*/

#include <Keypad.h>
#include <Servo.h>

const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {5, 4, 3, 2};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

Servo lockServo;
const int SERVO_PIN = 10;

String password = "1234";
String inputBuffer = "";

void setup() {
  Serial.begin(9600);
  lockServo.attach(SERVO_PIN);
  lockServo.write(0); // locked position
}

void loop() {
  // Handle password update command from Python
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd.startsWith("SETPASS:")) {
      password = cmd.substring(8);
      Serial.println("PASS_SET");
    }
  }

  char key = keypad.getKey();
  if (key) {
    if (key == '#') { // submit
      checkPassword();
      inputBuffer = "";
    } else if (key == '*') { // clear
      inputBuffer = "";
    } else {
      inputBuffer += key;
    }
  }
}

void checkPassword() {
  if (inputBuffer == password) {
    lockServo.write(90); // unlock
    Serial.println("UNLOCKED");
    delay(3000);
    lockServo.write(0); // relock
  } else {
    Serial.println("DENIED");
  }
}
