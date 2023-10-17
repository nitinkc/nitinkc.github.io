---
title:  "Asynchronous Programming"
date:   2023-10-10 15:16:00
categories: ['Java']
tags: ['Java']
toc: true
---


# Parallel vs Concurrent

# Parallel vs Asynchronous


Subroutine : Function you call and get a response

Coroutine : no entry point, no exit point. Just like a conversations

Continuations : 


# Parallel vs Concurrent

### Parallel

* Walk and Talk in parallel, exactly at the same time

```java
                          v
                          | Time Slice v
thread1        Talk   T   Talk   T
thread2        Walk       Walk
time  t=0-----------------^-------------------->t
```

### Concurrent

```java
                              v                    v
                              |Time slice          |Another timeslice
thread1              T   T   Talk           Talk   |      Talk
thread2                              Drink        Drink
time  t=0---------------------^--------------------^-------->t
```

# Parallel vs Asynchronous

Reactive Programming is equivalent to Functional programming ++

Asynchronous Programming : [vert.x library of Java](https://vertx.io/introduction-to-vertx-and-reactive/)

Asynchronous means `Non Blocking`
* --> Does not block the thread of execution and wait for that to finish.
* however, tasks are always blocking (default behaviour of a thread)
* what does the thread do : Thread to be non-blocking

* responsiveness : main thread should always deligate and be available for next step
    * Click on download button and then cancel
        * if main thread takes care od downloading, then the cancel button is blocked until the download is finished
* Pre-emptable :


Both parallel and Async processes run in a separate thread (other than main thread)

For parallel, the thread needs to **JOIN** i.e the slowest process/thread will determine the overall speed.
* pen refills (10), cap(20 per hour0  ) and body(50 body per hours) example. Total pens per hour = 10

* For Asynchronous, not waiting for completion, but when results does arrive, move on to do other things with it.
    * use the call back to receive response
    * Non blocking : when you make a call, you don't have to wait for it to complete.


**Concurrency** : looking for a new job, while working on the current job, during office hours.
**Parallelism** : maintaining 2 jobs, with 2 managers, without telling either manager
**Asynchronous** : While Brewing coffee, read emails and get back to coffee when its done.

# Async programming Features

**Call back** (Callback Hell) - When the response is received, execute the function
* ```java
    doSomething(data, response -> {...})
    ```
* CallBack lacks consistency
* Really hard to compose call backs
* hard to deal with error

> Callback hell to Promises

**Promise** : When done with the task, update through the promise by any one of the three states
* Pending
* Resolved
* Rejected

## CompletableFuture

CompletableFutures in Java is Promise in Javascript

{% gist nitinkc/17229c16e91766fa9eb903cad63a8def %}

{% gist nitinkc/eea4fd28d7765ec964cbf9b5c270ec5c %}

> Concurrency : looking for a new job while working in the current job -> concurrency.

> Working in 2 job together is parallel

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
