---
categories: Electronics
date: 2024-11-17 08:00:00
tags:
- Servo
- Motors
- Actuators
- Arduino
- Robotics
- Movement
title: Servo Motor
---

{% include toc title="Index" %}

Standard servo motor like the SG90 (quite common) and 
controlling it with the Servo library, 

```c 
#include <Servo.h>  // Include the Servo library

// Create a Servo object to control the servo
Servo myServo;

// Pin where the servo is connected
const int servoPin = 9;

void setup() {
  // Attach the servo to the pin
  myServo.attach(servoPin);

  // Optionally, you can start by setting the servo to a specific position
  myServo.write(90);  // Start at the middle position (90 degrees)
  delay(1000);         // Wait for 1 second
}

void loop() {
  // Sweep the servo from 0 to 180 degrees
  for (int degrees = 0; degrees <= 180; degrees = degrees + 15) {
    myServo.write(degrees);  // Move the servo to degree
    delay(15);            // Wait for the servo to reach the position
  }

  // Sweep the servo back from 180 to 0 degrees
  for (int pos = 180; pos >= 0; pos--) {
    myServo.write(pos);  // Move the servo to 'pos' degree
    delay(15);            // Wait for the servo to reach the position
  }
}
```

**Pin Connections**: Typically, the servo's signal pin (the control wire) is 
connected to a PWM-capable pin on the Arduino, such as pin 9 in this example. 
The power pin (VCC) goes to 5V, and the ground pin (GND) goes to GND on the Arduino.

Power Considerations: Servo motors can draw a lot of current, especially under
load. It's generally a good idea to power the servo directly from the 5V pin 
on the Arduino (if it’s a small servo) or 
use an external power supply if you are using a larger servo motor.