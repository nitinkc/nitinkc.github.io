---
categories:
- Electronics
date: 2024-10-25 22:00:00
tags:
- Basics
- Fundamentals
- Tutorial
- Getting Started
title: Electronics
---

{% include toc title="Index" %}

**Concepts**: Voltage, current, resistance.

# Ohm's Law
$ V = I \cdot R $

where:
- V is the voltage (in volts),
- I is the current (in amperes),
- R is the resistance (in ohms).

$$ R = \frac{V_{\text{source}} - V_f}{I_f} = \frac{5 \, \text{V} - 2.0 \, \text{V}}{0.020 \, \text{A}} = \frac{3.0 \, \text{V}}{0.020 \, \text{A}} = 150 \, \Omega $$ 

For a 5 Volt Supply, just choose a resistor greater than 150 Ohms. the larger the R, the dimmer the LED will be.


LED Voltage:

- WGB LED: 3.0V to 3.2V (average: 3.1V)
- RY LED: 2.0V to 2.2V (average: 2.1V)

| Supply Voltage (V)   | WGB LED Resistor (ohms)  | RY LED Resistor (ohms)   |
|:---------------------|:-------------------------|:-------------------------|
| 5                    | 95                       | 145                      |
| 10                   | 226                      | 390                      |
| 15                   | 357                      | 635                      |
| 20                   | 488                      | 880                      |

# Simple Parallel LED Circuit

# Simple Series LED Circuit