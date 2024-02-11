void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);  // Set the same Baud Rate as in MATLAB code

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("1");
  Serial.println("2");
  Serial.println("3");
  delay(random(250, 1000));
}
