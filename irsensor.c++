const int irSensorPin = 2;
int irSensorValue;

void setup() {
    Serial.begin(9600);
    pinMode(irSensorPin, INPUT);
}

void loop() {
    irSensorValue = digitalRead(irSensorPin);
    if (irSensorValue == HIGH) {
        Serial.println("Defective");
    } else {
        Serial.println("Okay");
    }
    delay(500);
}