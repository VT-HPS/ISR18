const int firstButtonPin = 4 ;
const int secondButtonPin = 3;
const int thirdButtonPin = 5;
int lastButton1State = LOW;
int lastButton2State = LOW;
int lastButton3State = LOW;
int debounceDelay = 25;
unsigned long firstButtonMillis = 0;
unsigned long secondButtonMillis = 0;
unsigned long thirdButtonMillis = 0;

void setup() {
  pinMode(firstButtonPin, INPUT);
  pinMode(secondButtonPin, INPUT);
  pinMode(thirdButtonPin, INPUT);
  Serial.begin(115200);  // Set the same Baud Rate as in MATLAB code

  firstButtonMillis = secondButtonMillis = thirdButtonMillis = millis();
}

void loop() {
  int reading1 = digitalRead(firstButtonPin);
  int reading2 = digitalRead(secondButtonPin);
  int reading3 = digitalRead(thirdButtonPin);

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

  if (reading3 != lastButton3State && (currentMillis - thirdButtonMillis) >= debounceDelay) {
    lastButton3State = reading3;
    thirdButtonMillis = currentMillis;
    if (lastButton3State == 1) {
      Serial.println("3");  // Send the activation state to MATLAB
    }
  }
}
