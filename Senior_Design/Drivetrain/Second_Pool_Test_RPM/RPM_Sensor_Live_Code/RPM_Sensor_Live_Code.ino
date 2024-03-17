const int firstButtonPin = 3;
const int secondButtonPin = 4;
int lastButton1State = LOW;
int lastButton2State = LOW;
int debounceDelay = 25;
unsigned long firstButtonMillis = 0;
unsigned long secondButtonMillis = 0;

void setup() {
  pinMode(firstButtonPin, INPUT);
  pinMode(secondButtonPin, INPUT);
  Serial.begin(115200);  // Set the same Baud Rate as in MATLAB code

  firstButtonMillis = secondButtonMillis = millis();
}

void loop() {
  int reading1 = digitalRead(firstButtonPin);
  int reading2 = digitalRead(secondButtonPin);

  unsigned long currentMillis = millis();

  if (reading1 != lastButton1State && (currentMillis - firstButtonMillis) >= debounceDelay) {
    lastButton1State = reading1;
    firstButtonMillis = currentMillis;
    if (lastButton1State == 1) {
      Serial.println("1");  // Send the activation state to MATLAB
    }
  }

  if (reading2 != lastButton2State && (currentMillis - secondButtonMillis) >= debounceDelay) {
    lastButton2State = reading2;
    secondButtonMillis = currentMillis;
    if (lastButton2State == 1) {
      Serial.println("2");  // Send the activation state to MATLAB
    }
  }
}
