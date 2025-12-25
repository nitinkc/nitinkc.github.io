---
title: Simple Drone
date: 2024-10-29 12:00:00
categories:
- Electronics
tags:
- DIY
---

{% include toc title="Index" %}

# Components Required
- Brushless Motors (2 pairs): One pair for the front and one for the back, with clockwise (CW) and counterclockwise (CCW) versions.
- Propellers (CW and CCW): Front and back propellers should be installed in opposite directions to counteract each other’s torque, which stabilizes the drone.
- Drone Frame: A small, lightweight frame to mount the motors and propellers. Can be ice cream stick
- Power Source and Control Board: A drone control board (like a flight controller) and battery are essential to manage motor speed and stabilize the drone.

# Mount the Motors:
Steps to Connect the Front and Back Propellers

**Reverse Polarity**:
To make the motor spin in the opposite direction, just swap the positive and negative connections of the motor.

# Attaching Propellers for Balanced Thrust
To ensure stable flight, match each motor with a compatible propeller designed for either clockwise (CW) or counterclockwise (CCW) rotation.

### Propeller Design:
- **Type A (CW)**: Spins clockwise; attach to motors that rotate clockwise.
- **Type B (CCW)**: Spins counterclockwise; attach to motors that rotate counterclockwise.

### Placement for Balanced Lift:
- Attach **CW** propellers to the **left front and right rear** motors.
- Attach **CCW** propellers to the **right front and left rear** motors.


This arrangement balances torque and ensures stable lift, enabling smooth and controlled drone flight.

# Connect Motors to Control Board:
Connect each motor to the drone control board according to the board’s motor layout.
- Adjust the settings to ensure each motor runs at the correct speed for stable hovering and maneuverability.

# Balance the Frame:
Check that the frame is balanced, with equal weight distribution for optimal control.

# Power
To power all four SHY-816 coreless motors simultaneously, 
you’ll typically use a parallel connection setup with a **3.7V** battery. Here’s a simple guide to wiring them:

Choose a Power Source:

Use a 3.7V LiPo battery with a sufficient capacity (e.g., 500mAh or higher) to support all four motors. 
Make sure the battery can handle the current required by the motors when they’re all running at the same time.

### Parallel Connection for Motors:

- Connect each motor’s positive terminal to the positive terminal of the battery.
- Connect each motor’s negative terminal to the negative terminal of the battery.

- This parallel wiring ensures each motor receives the same 3.7V from the battery.

## Use a Distribution Board or Soldering:

You can either solder the wires together or use a small power distribution board to
simplify connections and avoid soldering multiple wires to one point on the battery.

If soldering directly, it’s helpful to connect all positive leads together
and all negative leads together, then attach these bundles to the battery’
s positive and negative terminals, respectively.

Power Control:

If you need to turn all motors on and off at once, 
you could use a main switch or flight controller that connects between the battery and the motors.