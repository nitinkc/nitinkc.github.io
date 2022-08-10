---
title:  "Race Condition and Crtitcal Section"
date:   2022-08-06 08:30:00
categories: ['Java']
tags: ['Java']
---

As a general rule, you shouldn't expect to be creating your own interfaces, just to work with lambdas. T

The vast majority of likely operations, whether they have zero, one, or two arguments, including things dealing with
primitive return types, or primitive arguments, have probably been built for you.

And you should use the features of the java.util.function package when you need to create lambdas.

Concurrent systems -> different threads communicate with each other

Distributed Systems -> different processes communicate.

Concurrency vs parallelism



Reentreant Locks and Semaphores are introduced in Java 1.5

* Reentrant Locks (Mutex) allows only one thread in a critical section.
* Semaphore allows a fixed number of threads to access a critical section.
