---
categories: Performance Engineering
date: 2024-03-14 21:30:00
tags:
- Java
- Performance
- Debugging
title: Eclipse Memory Analyzer Tool (MAT)
---

{% include toc title="Index" %}

yCrash for all the tools under one bucket.

- MAT
- Visual VM
- JDK Mission Control

Use icon Assist : **⌥ Opt** + I or Help -> Icon Asist

![eclipse_mat.png](/assets/images/eclipse_mat.png)

Import the `.hprof` file

# Resource Leaks

Resource leaks don't generate explicit exceptions or errors like `IOException`
or `FileNotFoundException`.

Instead, they often lead to other kinds of issues that may be more challenging
to diagnose, such as:

**Memory Leaks**: If resources such as file handles, database connections, or
network sockets are not properly closed,
they can lead to memory leaks. Over time, this can exhaust system resources and
potentially cause OutOfMemoryError.

**Performance Degradation**: Leaked resources can cause performance issues.
For example, if file handles or database connections are not released,
it can slow down or even halt operations that require those resources.

**Resource Exhaustion**: Leaking resources might eventually lead to resource
exhaustion.
For instance, if a program continually opens file handles without closing them,
it could eventually run out of available file descriptors.