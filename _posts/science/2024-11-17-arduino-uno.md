---
title:  "Arduino UNO"
date:   2024-11-17 08:00:00
categories: [Electronics] 
tags: [Electronics]
---
{% include toc title="Index" %}

Arduino Uno has 14 digital I/O pins (0-13) and 6 analog pins (A0-A5). 

This sketch initializes all the pins and includes a basic setup for reference,
with comments on how you might handle different types of pins.

```c
#include <Wire.h> //for I2C communication
#include <SPI.h> //for SPI communication
#include <Servo.h> //for controlling servos
#include <LiquidCrystal.h> //for controlling LCD displays
#include <EEPROM.h> //for working with EEPROM storage
#include <SD.h> //for interfacing with an SD card
```

# Pin Definitions
```c
// Pin definitions
const int digitalPins[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};  // Digital I/O pins (0-13)
const int analogPins[] = {A0, A1, A2, A3, A4, A5};  // Analog pins (A0-A5)
```

# Debugging
```c
void setup() {
  // Start serial communication for debugging
  Serial.begin(9600);
  Serial.println("Print debug message");
}
```

# Set the pin mode 
- to be input or output
```c
void setup() {
    pinMode(digitalPins[i], OUTPUT);  // Set digital pins as OUTPUT
    digitalWrite(digitalPins[i], LOW); // Set them to LOW for safety
    
    pinMode(analogPins[i], INPUT);  // Set analog pins as INPUT
    
    // Configure pin 9 for PWM (Pulse Width Modulation)
    pinMode(9, OUTPUT);  // Pin 9 supports PWM
    Serial.println("Pin 9 initialized for PWM (Output)");
    
    // Configure pin 2 as an interrupt
  pinMode(2, INPUT_PULLUP);  // Enable internal pull-up resistor for interrupt-based usage
  Serial.println("Pin 2 initialized as INPUT_PULLUP for interrupt");
}
```
# Digital Pins (0-13):
- Pin 13: The Arduino Uno has a built-in LED connected to pin 13 often used for basic testing.
- Pins 2-13: These are general-purpose I/O pins that can be set as either INPUT or OUTPUT. 
- Pin 9 supports PWM (Pulse Width Modulation), so it can be used for dimming LEDs or controlling motors.

# Analog Pins (A0-A5):
- Analog pins (A0 to A5) are used for reading analog signals. 
- By default, they are in INPUT mode. 
- Read values from them using `analogRead()` and 
- write analog outputs using `analogWrite()` on PWM-capable pins.

# PWM Pins:
The Arduino Uno has PWM capabilities on pins 3, 5, 6, 9, 10, and 11. 
These pins can be used to create a **simulated analog output signal** using `analogWrite()`.

# Interrupts:
Pin 2 and Pin 3 on the Arduino Uno are capable of handling interrupts. 
You can use `attachInterrupt()` to trigger actions when a signal changes on these pins.

