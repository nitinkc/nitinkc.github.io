---
# layout: static
title:  "Virtual Threads in Java 21"
date:   2021-10-18 13:10:00
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

# Problems with Completablefutures

Railway track pattern is good in concept, but in implementation, 
* cognitive load : since there is skipping to then's or exceptionally's or the return type.

# Continuations and Coroutines

Don't want a Thread be blocked on a task. thread should be able to switch between the tasks

when a task is sleeping, thread should be able to do other things


**Subroutine** : Just a function, no state. Function you call and get a response.

**Coroutine** : Cooperative Routine - no entry point, no exit point. Just like a conversations. Kind of weave in and 
weave out of the functions.

**Continuations** : Data structure that helps to restore the context of a call between calls to a coroutine
* Should be a data structure that you benefit from but should not be directly accessed. Be in the background.
* Continuations in Java are behind the scenes.


```log
DONE in : Main thread Thread[#1,main,5,main]
entering task1 Thread[#1,main,5,main]
entering task2 Thread[#1,main,5,main] #when the task 1 goes to sleep, same thread picks up task2
exiting task2 Thread[#1,main,5,main]
exiting task1 Thread[#1,main,5,main] - Value of x = 90 #When the coroutine comes back to task1, it remembers the 
state and prints the value. This is done via continuations
```

Virtual threads occupy very small amount of memory and uses the concept of mounting and unmounting in terms of 
context switching when Sleep or blocking operation is involved.

Thread can switch between tasks


//Do not confuse ExecutorService with pooling
 bvc
No sense to pool virtual threads

VirtualThreads are like qtips - use and throw

# Two kinds of threads

### Platform threads
* the number of available platform threads is limited to the number of OS threads.
* typically have a large thread stack and other resources that are maintained by the operating system.

### Virtual Threads

* Virtual threads are suitable for running tasks that spend most of the time blocked, often waiting for I/O operations 
to complete. 
* However, they aren't intended for long-running CPU-intensive operations.

* Not managed or scheduled by the OS but the JVM is responsible for scheduling.
* any work must be run in a platform thread, but the JVM is utilizing **carrier threads**, which are 
  platform threads, to “carry” any virtual thread when its time has come to execute.
* All Virtual Threads are always daemon threads, don’t forget to call join() if you want to wait on the main thread.
* Available plentifully and can be used the **one thread per request** model
* If the code calls a blocking I/O operation in a virtual thread, the runtime **suspends the virtual thread** 
  which can be resumed which can be resumed at appropriate time later

* platform threads are managed in a **FIFO** work-stealing **ForkJoinPool**, 
  * uses all available processors by default
  * can be modified by tuning the system property `jdk.virtualThreadScheduler.parallelism`.

The main difference between a  and 

* the **common pool** that’s used by other features like parallel Streams operates in **LIFO** mode.
