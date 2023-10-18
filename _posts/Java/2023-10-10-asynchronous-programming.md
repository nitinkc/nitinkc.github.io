---
title:  "Asynchronous Programming"
date:   2023-10-10 15:16:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

Subroutine : Function you call and get a response

Coroutine : no entry point, no exit point. Just like a conversations

Continuations : 


Asynchronous Task Execution Engine -> Executor Service introduced in J1.5

It has

* Work Queue (Blocking Queue)
* Completion Queue
* Thread Pool

As soon as the work is placed in the work queue, you get Future. Future is a proxy or reference of the result that
will be returned in the Future

Fork Join Framework (used in parallel stream behind the scenes) -> Java 7 (Extends Executor service)


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

# Railway Track pattern

* treat error as another form of data and errors as first class citizens

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



# Parallel vs Asynchronous

Reactive Programming is equivalent to Functional programming ++

Asynchronous Programming : [vert.x library of Java](https://vertx.io/introduction-to-vertx-and-reactive/)

Non Blocking : when you make a method call, you dont have to wait for it to
complete

Asynchronous means `Non Blocking`
* --> Does not block the thread of execution and wait for that to finish.
* however, tasks are always blocking (default behaviour of a thread)
* what does the thread do : Thread to be non-blocking

* responsiveness : main thread should always deligate and be available for next step
    * Click on download button and then cancel
        * if main thread takes care od downloading, then the cancel button is blocked until the download is finished
* Pre-emptable :


Both parallel and Async processes run in a separate thread (other than main thread)

For parallel, the thread needs to **JOIN** i.e. the slowest process/thread will determine the overall speed.
* pen refills (10), cap(20 per hour0  ) and body(50 body per hours) example. Total pens per hour = 10

* For Asynchronous, not waiting for completion, but when results does arrive, move on to do other things with it.
    * use the call back to receive response
    * Non blocking : when you make a call, you don't have to wait for it to complete.


**Concurrency** : looking for a new job, while working on the current job, during office hours.
**Parallelism** : maintaining 2 jobs, with 2 managers, without telling either manager
**Asynchronous** : While Brewing coffee, read emails and get back to coffee when it's done.

# Async programming Features

**Call back** (Callback Hell) - When the response is received, execute the function
* ```java
    doSomething(data, response -> {...})
    ```
* CallBack lacks consistency
* Really hard to compose call backs
* hard to deal with error

CallBack
* CallBack lacks consistency
* Really hard to compose call backs
* hard to deal with error


> Callback hell to Promises

**Promise** : When done with the task, update through the promise by any one of the three states
* Pending
* Resolved
* Rejected

Promise
* resolve, reject or pending state
* 2 channels -> data channel & error channel


# CompletableFuture - ThreadPool

By Default Completable future uses the **Common ForkJoinPool**. Which means that the number of threads in a common
forkjoin pool is equal to the number of cores in the machine `Runtime.getRuntime().availableProcessors()`

Common ForkJoinPoll is shared by

* ParallelStreams
* CompletableFuture

And thus, user defined thread pool is also an option to avoid for resource waiting scenarios arising from common thread pool.

### Define User-defined threadpool

```java
Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors())
```



## CompletableFuture 
# CompletableFuture


CompletableFutures in Java is Promise in Javascript

##### Javascript code
Javascript is dynamically typed
{% gist nitinkc/17229c16e91766fa9eb903cad63a8def %}


| Current State | Next State | Function called            |
|:--------------|:-----------|:---------------------------|
| resolved      | resolved   | next then in the pipeline  | 
| resolved      | rejected   | next catch in the pipeline |
| rejected      | resolved   | next then in the pipeline  |
| rejected      | resolved   | next catch in the pipeline |

##### Java ()
Java is statically typed so we have to provide the type of CompletableFuture in the declaration
{% gist nitinkc/eea4fd28d7765ec964cbf9b5c270ec5c %}

> Concurrency : looking for a new job while working in the current job -> concurrency.

> Working in 2 job together is parallel

### CompletableFuture creation

#### Creating a completable future

{% gist nitinkc/7d0d331d4716151c51579d4fdda5ba94 %}


#### Creating a pipeline and then completing

{% gist nitinkc/da36ef99c6a7e383e7aea4475328ad9c %}

#### Dealing with Exceptions

# Exception handling with Completable Future

Three options available

* handle()
* exceptionally()

  The above two catches the exception and recovers

* whenComplete() -> Catches Exception but does not recover


with the use of exceptionally

* OK, go to the next THEN
* exception, go to the next EXCEPTIONALLY, 
    * BUT with proper type handling. The return type of Exceptionally has to be of the proper type. 
    * Write the exception code generically and use that so that it aligns to the data type properly.

##### Dealing with TimeOut
 2 functions
* completeOnTimeout - completeOnTimeout
* orTimeout

```java
private static void successOnTimeOut(CompletableFuture<Integer> future) {
  future.completeOnTimeout(5, 1, TimeUnit.SECONDS);//Does not keep the pipeline in PENDING state
        // for more than a second. the value doesn't arrive in 1 sec (timeout) then resolve it, via the default value
}
```

```java
private static void failureOnTimeOut(CompletableFuture<Integer> future) {
    future.orTimeout(1, TimeUnit.SECONDS);//Does not keep the pipeline in PENDING state
    //for more than a second. the value doesn't arrive in 1 sec (timeout) then resolve it, via the default value
}
```
### Stages of Completable futures

When one stage completes, another one starts and it keeps running

### supplyAsync()
* Factory method
* used to initiate asynchronous computations (tasks)
* takes **Supplier** as the input
* returns CompletableFuture<T>() of type T


### thenAccept()
* CompletionStage method
* used for chainign asynchronous tasks. has the capability to use the results of previous asynck ask and perform actions on it
* takes **Consumer** as the input
* returns CompletableFuture<Void>() type Void


### thenApply()
* Completion Stage method
* used for applying transformations, takes a Function
* thenApply deals with **Function that returns** a value
* returns CompletableFuture<T>() of TypeT

##### thenApply()

* Completion Stage method
* used for applying transformations, takes a Function
* thenApply deals with **Function that returns** a value
* returns CompletableFuture&lt;T>() of TypeT

##### Combine
Use Case : When there is a need to bring data from multiple microservices and cvombine then

{% gist nitinkc/124fce7e90ac53e72f3d45f014d8a88b %}

##### thenCombine()
* used to combine Independent Completable Futures
* Takes two arguments
  * CompletionStage,
  * BiFunction
* Returns a CompletableFuture

### thenCombine()
* combines independent CompletableFutures (Async Tasks)
* For Example : if a service makes 2 calls to independent services, then the total latency will be MAX(service1, service2) instead of SUM(service1, service2)
* takes 2 arguments, CompletionStage and BiFunction
* returns CompletableFuture

##### Compose 

##### thenCompose()

* Completion Stage method
* Transform data from one form to another
* Input is a `Function` functional interface
* Deals with methods that return completableFuture


### thenCompose()
* Completion Stage method
* used for applying transform one data to another, takes a Function
* deals with functions that **returns CompletableFuture<T>**
* thenCompose depends on the completion of the dependent Future task











| Functional Interface | Method         | Streams API | Async API     |
|:---------------------|:---------------|:------------|:--------------|
| Predicate &lt;T>     | boolean test() | filter()    |               |
| Function<T,R>        | R apply(T k)   | map()       | thenApply()   |
| Consumer&lt;T>       | void accept(T) | forEach()   | thenAccept()  |
| Supplier&lt;T>       | T get()        | Factories   | supplyAsync() |





| Streams                | CompletableFuture                  | 
|:-----------------------|:-----------------------------------|  
| Zreo, one or more data | zero or one                        |
| only data channel      | data channel or error channel      |
| pipeline & lazy        | pipeline & lazy                    |
| Exception - nope       | error channel                      |
| forEach                | thenAccept                         |
| map                    | thenApply - perform transformation |
| ((( zip )))            | thenCombine                        |
| flatMap                | thenCompose                        |


Function returning data -> map
Function returning Stream -> flatMap

Function returning data -> thenAccept/thenApply
Function returning CompletableFuture -> thenCompose