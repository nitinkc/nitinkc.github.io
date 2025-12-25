---
categories: Electronics
date: 2024-11-03 01:00:00
tags:
- Soft Starter
- Motor Control
- Power
- Circuit
- Inrush Current
title: Soft Starter
---

{% include toc title="Index" %}


# Slow starter for DC motor - soft start

```markdown
Power + ---- Resistor ----+---|diode>|----+ Motor +
                            |           |
                            +---+---+       |
                            |  C1   |       |
                            |  C2   |       |
                            |  C3   |       |
                            +-------+       |
                            GND         GND
```

## Components
- Capacitors (3 x 100µF): These capacitors will gradually charge, controlling the slow-start behavior by slowly increasing the voltage across the motor.
- Resistor (R): Controls the charging speed of the capacitors.
- Diode (D): Prevents the capacitors from discharging back into the power source.

## Circuit Diagram

- Power Source: Connect the positive terminal of the power source to one end of the resistor.
- Resistor: Connect the other end of the resistor to the anode of the diode and to one terminal of each capacitor.
- Capacitors: Connect the three capacitors in parallel (positive terminals together and negative terminals together).
- Diode: Connect the cathode (striped side) of the diode to the motor’s positive terminal.
- Motor: Connect the motor's negative terminal to ground.

# Option 2: Improved Slow Start Circuit (Two Resistors, One Diode)
Resistor 1: Connects between the power source and the capacitors to control the charge rate (similar to Option 1).

Resistor 2: Connects in parallel with the motor to control the discharge rate of the capacitors when the power is turned off. This can help the capacitors discharge more evenly, readying them for the next start-up.

In the Option 2 setup, you might use one diode between the resistor-capacitor section and the motor to block any unwanted discharge into the motor once it’s running.