---
title:  "Asynchronous Programming"
date:   2023-10-10 15:16:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

**Concurrency** : looking for a new job, while working on the current job, during office hours.
**Parallelism** : maintaining 2 jobs, with 2 managers, without telling either manager
**Asynchronous** : While Brewing coffee, read emails and get back to coffee when it's done.

# Parallel vs Concurrent

**Parallel**

* Walk and Talk in parallel, exactly at the same time

```java
                          v
                          | Time Slice v
thread1        Talk   T   Talk   T
thread2        Walk       Walk
time  t=0-----------------^-------------------->t
```

**Concurrent**

```java
                              v                    v
                              |Time slice          |Another timeslice
thread1              T   T   Talk           Talk   |      Talk
thread2                              Drink        Drink
time  t=0---------------------^--------------------^-------->t
```


# Parallel vs Asynchronous

Asynchronous means `Non Blocking`

* Non Blocking : when you make a method call, you dont have to wait for it to complete
* Does not block the thread of execution and wait to finish.
* however, tasks are always blocking (default behaviour of a thread)
* what does the thread do : Thread to be non-blocking
  * responsiveness : main thread should always delegate and be available for next step
      * Click on download button and then cancel
          * if main thread takes care of downloading, then the cancel button is blocked until the download is finished
  * Pre-emptible :


>Both parallel and Async processes run in a separate thread (other than main thread)

For parallel, the thread needs to **JOIN** i.e. the slowest process/thread will determine the overall speed.
* pen refills (10), cap(20 per hour0  ) and body(50 body per hours) example. Total pens per hour = 10

* For Asynchronous, not waiting for completion, but when results does arrive, move on to do other things with it.
    * use the call back to receive response
    * or use a promise


## Asynchronous Task Execution Engine 

-> Executor Service introduced in Java 1.5

It has

* Work Queue (Blocking Queue)
* Completion Queue
* Thread Pool

As soon as the work is placed in the work queue, you get Future.
Future is a proxy or reference of the result that will be returned in the Future

Fork Join Framework (used in parallel stream behind the scenes) -> Java 7 (Extends Executor service)


# Async & non blocking programming Features

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

Promise has 2 channels -> data channel & error channel

## Railway Track pattern

Treat error as another form of data and as first class citizens

```java
data track  -----f------f     recovering from exception       f--or continue with then methods-----
                          \                                  /
error track ----------------f---can retrun default data-----f----or handle exception---------------
```

```java
HappyPath==========================D==========D=======================
data -> function -> Promise -> f-> P -> f  -> P -> f -> P -> f-> P -> f       
UnhappyPath===========================================Exception==E=======

```

# CompletableFuture

CompletableFutures in Java is the same as Promise in Javascript

##### Javascript code
Javascript is dynamically typed
{% gist nitinkc/17229c16e91766fa9eb903cad63a8def %}

| Current State | Next State | Function called            |
|:--------------|:-----------|:---------------------------|
| resolved      | resolved   | next then in the pipeline  | 
| resolved      | rejected   | next catch in the pipeline |
| rejected      | resolved   | next then in the pipeline  |
| rejected      | resolved   | next catch in the pipeline |

##### Java
Java is statically typed, so we have to provide the type of CompletableFuture in the declaration
{% gist nitinkc/eea4fd28d7765ec964cbf9b5c270ec5c %}


# CompletableFuture - ThreadPool

By Default Completable future uses the **Common ForkJoinPool**. 
Which means that the number of threads in a common forkjoin pool is equal to the number of cores
in the machine `Runtime.getRuntime().availableProcessors()`

Common ForkJoinPool is shared by

* ParallelStreams
* CompletableFuture

And thus, **user defined thread pool** is also an option to avoid for resource waiting scenarios arising from common thread pool.

Define User-defined thread pool
```java
Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors())
```

### Creating a completable future

{% gist nitinkc/7d0d331d4716151c51579d4fdda5ba94 %}


### Creating a pipeline and then completing

{% gist nitinkc/da36ef99c6a7e383e7aea4475328ad9c %}


# Stages of Completable futures

When one stage completes, another one starts and it keeps running

### supplyAsync()
* Factory method
* used to initiate asynchronous computations (tasks)
* takes **Supplier** as the input
* returns `CompletableFuture<T>()` of type T

### thenAccept()
* CompletionStage method
* used for chainign asynchronous tasks. has the capability to use the results of previous async task and perform 
  actions on it
* takes **Consumer** as the input
* returns `CompletableFuture<Void>()` type Void

### thenApply()
* Completion Stage method
* used for applying transformations, takes a Function
* thenApply deals with **Function that returns** a value
* returns `CompletableFuture<T>()` of TypeT

### thenCombine()
Use Case : When there is a need to bring data from multiple microservices and combine them

* used to combine Independent Completable Futures (two asynchronous tasks)
  * For Example : if a service makes 2 calls to independent services, then the total latency will be MAX(service1, 
  service2) instead of SUM(service1, service2)
* Takes two arguments - `thenCombine(CompletionStage, BiFunction)`
  * CompletionStage,
  * BiFunction
* Returns a CompletableFuture

{% gist nitinkc/124fce7e90ac53e72f3d45f014d8a88b %}

### thenCompose()
* compose() is used for transforming the result of one CompletableFuture into another CompletableFuture.
* used to chain two asynchronous operations where the second depends on the result of the first.
* The function provided to compose() maps the result of the first CompletableFuture to a new CompletableFuture.
* thenCompose depends on the completion of the dependent Future task
* Completion Stage method
* Input is a `Function` functional interface, Transform data from one form to another
* returns **CompletableFuture<T>** here T is the type of the result of the second CompletableFuture. 
* The resulting CompletableFuture is a flattened chain.

### Exceptionally

With the use of **exceptionally** if the execution of the task is
* OK, go to the next THEN
* exception, go to the next EXCEPTIONALLY, 
    * BUT with proper type handling. The return type of Exceptionally has to be of the proper type. 
    * Write the exception code generically and use that so that it aligns to the data type properly.

compose() --> sequencing dependent asynchronous tasks, 
thenCombine() --> combine the results of two independent asynchronous tasks into a single result
{: .notice--primary}

### Dealing with TimeOut
 2 functions

##### completeOnTimeout

if the CompletableFuture doesn't complete within the specified timeout, it will be completed with the provided default 
value.

```java
private static void successOnTimeOut(CompletableFuture<Integer> future) {
  future.completeOnTimeout(5, 1, TimeUnit.SECONDS);//Does not keep the pipeline in PENDING state
        // for more than a second. the value doesn't arrive in 1 sec (timeout) then resolve it, via the default value
}
```

##### orTimeout

If the CompletableFuture times out, it is canceled, and the resulting CompletableFuture is considered completed 
exceptionally with a TimeoutException.

* it can interrupt the underlying task if it takes too long to complete. 

```java
private static void failureOnTimeOut(CompletableFuture<Integer> future) {
    future.orTimeout(1, TimeUnit.SECONDS);//Does not keep the pipeline in PENDING state
    //for more than a second. the value doesn't arrive in 1 sec (timeout) then cancel it, and completes it exceptionally with a TimeoutException
}
```

### join()

* to obtain the result of the asynchronous computation when it's done.
* similar to the get() method, but doesn't throw checked exceptions.
* waits indefinitely for the computation to finish 
  * returns the result 
  * or throws any unhandled exception if one occurs.

```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> 100);
int result = future.join(); // Get the result when the computation is complete
```

### get()

* like join(), the get() method is also used to obtain the result of the asynchronous computation when it's done.
* Unlike join(), the get() method can throw checked exceptions, specifically `InterruptedException` and 
  `ExecutionException`, which need to be handled.
* use get() if there is a need to handle exceptions or have more control over waiting for the result.

```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> 100);
try {
    int result = future.get(); // Get the result and handle exceptions
} catch (InterruptedException | ExecutionException e) {
    // Handle exceptions
}
```

### complete(T value):

* allows to manually complete a CompletableFuture with a specific result value.
* to provide a result explicitly, bypassing the actual asynchronous computation.

{% gist nitinkc/28618b6feb55df00447289a75b351dba %}

# Streams API vs Async API

| Functional Interface | Method         | Streams API | Async API     |
|:---------------------|:---------------|:------------|:--------------|
| Predicate &lt;T>     | boolean test() | filter()    |               |
| Function<T,R>        | R apply(T k)   | map()       | thenApply()   |
| Consumer&lt;T>       | void accept(T) | forEach()   | thenAccept()  |
| Supplier&lt;T>       | T get()        | Factories   | supplyAsync() |

# Streams vs CompletableFuture

| Streams                  | CompletableFuture                       | 
|:-------------------------|:----------------------------------------|  
| Zreo, one or more data   | zero or one                             |
| only data channel        | data channel or error channel           |
| pipeline & lazy          | pipeline & lazy                         |
| Exception - nope         | error channel                           |
| forEach                  | thenAccept (consumes data)              |
| map                      | thenApply - perform transformation      |
| ((( zip )))              | thenCombine                             |
| flatMap (returns Stream) | thenCompose (returns CompletableFuture) |