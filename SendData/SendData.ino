/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/
int brightness = 0;
int led = 6;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  int millivolt = map(sensorValue, 0, 1023, 0, 5000);
  float tempC = (millivolt - 750.0)/10 + 25;
  float tempF = (tempC * 1.8) + 32;
  // print out the value you read:
  Serial.println(tempF);
  if(Serial.available() > 0) {
        brightness = Serial.parseInt();
      }
      analogWrite(led, brightness);
  delay(10000);        // delay 10s
}
