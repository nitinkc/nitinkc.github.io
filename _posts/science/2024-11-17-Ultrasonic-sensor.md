---
categories:
- Electronics
date: 2024-11-17 08:00:00
tags:
- Sensors
- Arduino
- Projects
title: Ultrasonic Sensor
---

{% include toc title="Index" %}

Ultrasonic sensor (HC-SR04):
VCC -> 5V (Arduino)
GND -> GND (Arduino)
Trig -> Pin 9 (Arduino)
Echo -> Pin 10 (Arduino)

# Measure Distance with an Ultrasonic Sensor
```c  
#define TRIG_PIN 9   // Pin connected to the Trig pin of the ultrasonic sensor
#define ECHO_PIN 10  // Pin connected to the Echo pin of the ultrasonic sensor

void setup() {
  // Start serial communication
  Serial.begin(9600);

  // Set the Trig and Echo pins as OUTPUT and INPUT
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  // Clear the Trig pin (set to LOW)
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2); // Wait for 2 microseconds to ensure a clean LOW signal
  
  // Send a 10-microsecond pulse to trigger the ultrasonic burst
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure the time it takes for the echo to return
  long duration = pulseIn(ECHO_PIN, HIGH); // Pulse duration in microseconds

  // Calculate the distance based on the speed of sound (343 m/s or 0.034 cm/µs)
  // Distance = (Time * Speed of sound) / 2
  // We divide by 2 because the pulse travels to the object and back (round-trip)
  long distance = (duration * 0.034) / 2;  // Distance in centimeters

  // Print the distance to the Serial Monitor
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Wait a short time before taking the next reading
  delay(500);
}
```