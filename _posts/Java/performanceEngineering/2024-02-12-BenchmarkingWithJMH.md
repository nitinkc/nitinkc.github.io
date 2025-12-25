---
title: Java Mission Control - JMC
date: 2024-02-17 12:40:00
categories:
- Performance Engineering
tags:
- Java
- Profiling
- Performance
- Monitoring
- Tools
---

{% include toc title="Index" %}

JMH is more suited for microbenchmarking Java code rather than making HTTP
requests.

# Profiling Tools:

- VisualVM: A free tool provided by Oracle that integrates with the JDK. It
  provides CPU, memory, and thread profiling.
- Eclipse Memory Analyzer (MAT): A powerful tool for analyzing Java heap dumps.
- JProfiler: A commercial Java profiler that provides detailed memory analysis.
- YourKit: Another commercial profiler with advanced memory profiling
  capabilities.

# JVM Monitoring Tools:

- JConsole: A monitoring tool that comes with the JDK, providing basic profiling
  features.
- Java Mission Control (JMC): A profiling and diagnostics tool that comes with
  the Oracle JDK.

[JDK Mission Control (JMC) 8 Downloads](https://www.oracle.com/java/technologies/javase/products-jmc8-downloads.html)

The app can be extracted and be used directly.