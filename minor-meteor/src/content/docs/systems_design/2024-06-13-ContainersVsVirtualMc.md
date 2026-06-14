---
title: Containers vs Virtual Machine
date: 2024-06-13 11:02:00
categories:
- System Design
tags:
- Containers
- Infrastructure
---

{% include toc title="Index" %}

![](https://www.youtube.com/watch?v=Jz8Gs4UHTO8&t=307s)
Bare Metal : Physical computer/server

Virtual Machine : Emulation of physical machines
hardware -> Host operating system -> Hypervisor -> virtual machines

hardware -> bare metal hypervisor -> virtual machines

- high performance
- high cost of hardawre that supports bare metal hypervisor

Virtual machines are vulnerable to noise neighbour problems

Containerization : light weight Virtulization

hardware -> host operating system -> container Engine -> containers

# Container

A container is a bundling of an application and all its dependencies as a
package
that allows it to be deployed easily and consistently regardless of the
environment.

- container use Virtualization features of the host operating system.