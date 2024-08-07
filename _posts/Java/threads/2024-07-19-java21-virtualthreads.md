---
title:  "Virtual Threads"
date:   2024-07-19 12:17:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

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
* All Virtual Threads are **always daemon threads**, don’t forget to call `join()` if you want to wait on the main thread.
* Available plentifully and can be used the **one thread per request** model
* If the code calls a blocking I/O operation in a virtual thread, the runtime **suspends the virtual thread**
  which can be resumed which at appropriate time later

* platform threads are managed in a **FIFO** work-stealing **ForkJoinPool**,
    * uses all available processors by default
    * can be modified by tuning the system property `jdk.virtualThreadScheduler.parallelism`.

* the **common pool** that’s used by other features like parallel Streams operates in **LIFO** mode.

The Virtual Thread uses :-
- Continuations
- Executor Service
- ForkJoinPool

# Task Types
- IO Bound
- CPU Bound

## Handling the user requests
A couple of different architectures used by application servers for handling the user requests.
- process-per-request model (old, CGI - Common Gateway Interface)[https://en.wikipedia.org/wiki/Common_Gateway_Interface]
- thread per request model

In the 1990s, a popular mechanism for handling user requests was the CGI, the common gateway interface.
In this architecture, when a user sends a request to the web server, the web server will invoke the associated CGI script
as a separate **process**.

Once the response is sent back, the process is destroyed and this is an overhead.

This is an issue because a process in an operating system is considered heavyweight, starting and terminating a process for every request is inefficient.

So because of this, a variation of CGI was created and that is called fast CGI.
- like having a pool of processes, and the user request is routed to one of the available processes.
- There is no extra time spent on starting up a new process because it's already up.

# Concurrency and Parallelism

##  Parallelism
- Multiple dependent sub tasks - all executing at the same time
- Multiple cores involved
- No parallelism in single core

```markdown
      Task
      |
  --------------
  |    |    |    |
Sub Sub  Sub  Sub
task task task task
  1    2    3    4
  |    |    |    |
Core Core Core Core
  1    2    3    4
```

# Blocking vs Non blocking IO
**IO opearations**
- socket reads/writes - used by DB calls, REST Calls, anything to do with the networks
- file reads/writes - disk/slower memory access
- concurrent locks - enforcing synchronization

Reactive Programming : to overcome scalability problems with IO
{: .notice--info}

**Blocking IO aka synchronous I/O**

In Blocking-I/O operations, a thread that performs an I/O operation (such as reading from a file or network socket) is 
**blocked** until the operation completes. During this time, the thread cannot perform other tasks. 
- This is a performance blocker

**Synchronous call**

```mermaid!
sequenceDiagram
  participant Client
  participant API1
  participant API2
  participant ExternalSystem

  Client ->> API1: Call API1
  Note over Client, ExternalSystem: Blocking I/O operation
  API1 ->> ExternalSystem: Request data
  ExternalSystem -->> API1: Response data
  API1 -->> Client: Response from API1
  Client ->> API2: Call API2
  API2 -->> Client: Response from API2
```

**Non Blocking IO**

In non-blocking I/O operations, a thread initiates an I/O operation and continues executing other code while the 
I/O operation is processed asynchronously.
- This can improve performance and scalability, especially in systems with high I/O operations.

**Asynchronous calls**
- Futures and Callbacks

```mermaid!
sequenceDiagram
    participant Client
    participant API1
    participant API2

    Client ->> API1: Call API1 (Async)
    API1 -->> Client: Acknowledge receipt
    Client ->> API2: Call API2 (Async)
    API2 -->> Client: Acknowledge receipt
   
    Note over Client, API2: Responses can be received in any order
    API2 ->> Client: Response from API2
    API1 ->> Client: Response from API1
```

![blockingVsNonBlocking.png](..%2F..%2Fassets%2Fimages%2FblockingVsNonBlocking.png)


In Java 1MB of Stack is allocated for each thread. That's mandated by the OS because,
the Java thread is backed by the OS thread, which requires memory up front.

Note: the Java threads are basically a thin layer on top of the OS Threads, so creating a Java thread creates an underlying OS thread under the hood.
{: .notice--info}

# Project Loom & Virtual threads
Most fundamental change in Java
- The Virtual thread starts as a Daemon thread whereas the platform thread starts as a non-daemon thread
- The JVM Shutsdown when there are no non-daemon threads running.
- error with platform thread with large number of threads
```
[3.536s][warning][os,thread] Failed to start thread "Unknown thread" - pthread_create failed (EAGAIN) for attributes: stacksize: 1024k, guardsize: 4k, detached.
[3.536s][warning][os,thread] Failed to start the native thread for java.lang.Thread "Thread-8158"
```
- With Virtual threads, each worker/task corresponds to one platform thread. 
- Each worker just runs and leaves and picks other task, thus starting and ending of a same methods can be done in different threads.

the virtual thread `#31` is started by the `worker2` but is ended by the `worker4`.
```
Start::executeBusinessLogic : VirtualThread[#31]/runnable@ForkJoinPool-1-worker-2
Start::executeBusinessLogic : VirtualThread[#29]/runnable@ForkJoinPool-1-worker-1
END::executeBusinessLogic : VirtualThread[#31]/runnable@ForkJoinPool-1-worker-4
END::executeBusinessLogic : VirtualThread[#29]/runnable@ForkJoinPool-1-worker-3
```

# Virtual Thread creation
Virtual Threads are scheduled on a platform thread (aka carrier thread) for its CPU bound operation.

The big advantage is that when we use virtual threads, the OS thread is released automatically during an IO operation.

### Using static thread method
- can't name a thread 
```java
var t = Thread.startVirtualThread(() -> executeBusinessLogic());
//Make sure that the thread terminates before moving on
t.join(); //Proceed sequentially after thread completes its task
```

### Create a virtual thread builder object
Builder is **NOT** Thread Safe
{% gist nitinkc/b682bc6e3e3dbdb83322c940c00d0267 %}

### Using Thread factory
 is thread safe
{% gist nitinkc/cb1f98eb47895a4388e4b685a9792d65%}

### Using the virtual thread executor service
{% gist nitinkc/96904758c763e2c43b6f9fdd8898e668%}

### Thread Per Task Executor Service
{% gist nitinkc/ddebd32d96b28d62f7fc20ddeb8336fa %}

### try with resource block
Simplifies the code because no need to join the threads.

Waiting for all threads to complete involves
- creating an array of threads and 
- joining with each of them explicitly. 

In JDK 21 (officially supporting Virtual threads), the ExecutorService is "**Autocloseable**". 

which means if you use the try with resource block, the close method will be called on the ExecutorService 
at the end of the block and this will wait till all the virtual threads are terminated.

This is one example of "Structured Concurrency" where we wait for all threads started within a block to complete, 
so that there are no rogue runaway threads.

# Scenario
When there are multiple independent tasks to be completed, all as part of one thread, without blocking the thread
> Concurrently run many tasks within a thread in non-blocking fashion

combination of using virtual threads to write sequential code and futures/CompletableFutures for 
concurrent code is both readable and powerful
{: .notice--primary}

Whenever we need a new thread, we simply **create a new virtual thread** without worrying about resources 
as virtual threads are cheap and efficient.

There is no harm in writing blocking code within a virtual thread.
- Since there are no platform thread which holds on to the resources
- as it managed and released by the JVM

Writing non-blocking code with Reactive frameworks like project Reactor or CompletableFutures makes the readability hard

But, if we want sophisticated mechanisms to deal things in pipeline with exception handling and error handling mechanism, 
the CompletableFutures is a good optipn

{% gist nitinkc/d218df71705ab37a711ccc6ac32ebe06%}

# Virtual Threads with ForkJoinPool
![virtualthreadWithFJPool.png]({{ site.url }}/assets/images/virtualthreadWithFJPool.png)