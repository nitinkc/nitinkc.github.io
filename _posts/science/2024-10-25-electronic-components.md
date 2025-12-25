---
title: Electronic Components
date: 2024-10-25 12:00:00
categories:
- Electronics
tags:
- Components
- Reference
- Guide
---

{% include toc title="Index" %}

# 1. **Supplies**
- AA batteries (or a small rechargeable battery pack).
- Breadboard and jumper wires.
- Soldering supplies (if applicable).
- **Basic tools**: wire strippers, multimeter, etc.

## Power Supply - From USB Mobile Charging Cable
Cut the end that is used for mobile charging and pull out the outer layer to expose 4 wires underneath.

- The **Red** wire acts as **Anode(+ve)** while 
- the **Black** is used as **Cathode(-ve)/Ground**.

Then use the USB input end to connect with either Laptop or charging port or any power supply to avoid using batteries.

## Step Up/Down Power Supply Module
Adjustable Boost Buck Converter 1.2V-24V Output

Use the mini circuit board with adjustable power supply

# RGB multicolor LED
An RGB multicolor LED can come in two configurations: **common cathode** and **common anode**. 

### Common Cathode RGB LED
Configuration:
- In a common cathode RGB LED, all the cathodes (negative terminals) of the red, green, and blue LEDs are connected together and typically connected to ground (0V).
- Each of the anodes (positive terminals) of the individual LEDs is connected to a control signal or a resistor, which allows you to control the brightness and color by varying the voltage applied to each anode.

Pin Configuration:
- Pin 1: Red Anode
- Pin 2: Green Anode
- Pin 3: Blue Anode
- Pin 4: Common Cathode (connected to ground)

Operation:
By applying a voltage to one or more of the anodes while keeping the common cathode grounded, you can mix the colors:
Red: Turn on the red anode.
Green: Turn on the green anode.
Blue: Turn on the blue anode.
Mixing Colors: Combine different intensities of red, green, and blue to create various colors (e.g., yellow = red + green, cyan = green + blue, magenta = red + blue).

## Bench Power Supply

# 2. **Basic Components**
- Resistors (various values).
- Capacitors (e.g., 10µF, 100µF).
- LEDs (various colors).
- Diodes (1N4148 or similar).
  - Zeiner Diode - gets activated with a certain voltage

## Simple LED 0.3 or 0.5 mm
- longer leg - positive side/Anode
- shorter leg - negative side/Cathode
  - if inner filament is visible, the larger one is cathode
  - if the filament is not visible & legs are already cut,
    - then locate the flat edge on the round base of the LED

![Led diode anode cathode ](https://www.robot-maker.com/shop/img/cms/tuto-led/ledwiring.jpg)
 
-Forward Voltage (V<sub>f</sub>): Appx. voltage of the LED is 2.0V (common for red LEDs).
- Forward Current (I<sub>f</sub>): Typically around 20 mA (0.020 A)

# 3. **Switches**
- Push-button switches.
- Toggle switches, banana switches

# 4. **Transistors**
- NPN (like 2N3904) and PNP (like 2N3906) transistors.
  The **TO-92** is a transistor package type commonly used for small, low-power transistors.
  It’s a **plastic-encapsulated package** with a distinctive shape that looks like a small
  cylinder with a flat edge on one side.

# Active Components vs Passive

| **Component Type**  | **Examples**                     | **Function**                       | **Power Requirement**           |
|:--------------------|:---------------------------------|:-----------------------------------|:--------------------------------|
| **Active**          | Transistors, ICs, Op-Amps        | Amplify, switch, generate signals  | Needs an external power source  |
| **Passive**         | Resistors, Capacitors, Inductors | Store or dissipate energy, filter  | No external power source needed |


# 5. **Integrated Circuits**
- 555 timer IC.
- Simple logic gate ICs (like AND, OR).

# 6. **Sensors**
- Photoresistor (LDR).
- Temperature sensor (LM35 or similar).

### IR Sensor
IR LEDs typically operate at wavelengths between **700 nm and 1 mm**, 
depending on the specific type and application.

-  IR Transmitter : **IR LED** - Emits infrared light.
- IR Receiver : **IR Photodiode or Phototransistor** - Detects the infrared light and 
converts it back into an electrical signal.

# 7. **Motors**
- Small DC motors.
- Servo motors.
- brushless DC motor - Drone motor with Type A and B fans