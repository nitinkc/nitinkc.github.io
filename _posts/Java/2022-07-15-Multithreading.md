---
# layout: static
title:  "Multithreading & CompletableFuture"
date:   2021-10-13 21:55:00
categories: ['Java']
tags: ['Java']
---


## History of multithreads

Java 1 : Threads -> one set of API for all machines. hardware independent

Java 5 : ExecutorServices API -> Pool of threads
* Issue 1: Pool induced deadlock
* One thread breaks the problem and throws in the pool and waits foe the result to come back
* All the threads in pool just divided the work, and no thread left to take care of the problem

Java 7 : Fork Join pool
* Work-stealing : the threads that divides problem, also solves one of the divided part

Java 8 : ParallelStreams and CompletableFutures
* uses Java 7 FJP
* Common Fork join pool

Java 21 : Virtual Threads
* dsfgds

