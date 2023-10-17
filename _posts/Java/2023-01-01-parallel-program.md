---
title:  "Parallel Streams"
date:   2023-01-01 18:10:00
categories: ['Java']
tags: ['Java']
toc: true
---

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


## Parallel Streams

Martin Fowler : Collection pipeline pattern

* Imperative style has accidental complexity
  * Converting a for loop is a nighmare to convert it onto parallel program.
  * unnecessasary complexity trying to synchronize and parallelize
    * Structure of program needs to be changed
* Functional style has less complexity. The codes well explaining business logic. 
  * Easier to parallelize
  * maintainable: Structure remains the same, just parallel gets added


* Mutability and parallelism doesn't go together. Watch mutability


With Pipeline pattern, just change the stream to parallelstreams whihc can parallelize the code.

Only requirement is
    Lambda should a pure function. No shared mutability


`stream.parallel()` when the source is outside and forced to use stream after it has been created

`parallelStream()` when you are the source of the stream

Be Careful of `sequential()` right before the terminal operation.

Intermediate operations returns stream and evaluated lazily
Terminal operation gets evaluated right on time

```java
list.parallelStream()
    .map(num -> incrementWith1SecDelay(num))
    .sequential()//This takes precedence due to its proximity with forEach (Reduce operation)
    .forEach(num -> System.out.print(num+" "));
```

| Streams                                          | Reactive Streams                                   | 
|:-------------------------------------------------|:---------------------------------------------------|  
| Sequential vs parallel                           | Synchronous vs Asynchronous                        |
| Entire pipeline is either sequential or parallel | Depends                                            |
| no segments                                      | subscribeOn - no segements \n onserveOn = segments |




## Order of execution

Use of forEachOrdered. The execution happens parallel, but the for each run after all the threads are completed

```java
list.parallelStream()//Simple conversion to parallel stream
      .map(num -> incrementWith1SecDelay(num))
      .forEachOrdered(num -> System.out.print(num+" "));//Enforces Ordering on the consumer function being passed
```

* forEach is unordered. 
* forEachOrdered does not impose only ordering, not sequential ordering
* forEachOrdered can guarantee ordering to only ordered streams. Eg: list can be ordered, but set cannot
* The order is the order in which the elements **appear** in the collection (**insertion order** NOT the sort order)


## Parallel and Reduce

filter and map runs parallel without issues.


first argument in reduce is not inital value

```java
Integer result = list
      .parallelStream()//Using Parallel Stream
      .reduce(1, //First Parameter is not INITIAL value, it's an identity
              (total, e) -> add(total, e));//Returns 345 for a list of 1 to 10
```
Reduce does nto take an initial value, it takes an identity value

* integer and + -> identity  = 0
* integer and * -> identity  = 1

Should be a monoid 
  * there should be an identity values  
  * the operations performed should result the values should belong to the same set

## # of Threads

The total number of thread creation depends upon the task. But `# of threads <= # of cores`

IO intensive Problem vs Computationally intensive problem

Computationally intensive
  number of threads should be less than or equal to number of cores

For IO Intensive
   number of threads may be greater than number of cores. 

Consider the equation

`# of threads = # of cores / (1 - blocking factor)`

For IO intensive tasks, the blocking factor is usually large. The thread keep waiting for longer duration 
and that waiting time can be utilized by the CPU for some other task

for example of the thread is waiting for half the time which is 50%, the blocking factor is 0.5 and the number of threads
will be double the number of CPU cores, thus in effect twice the number of threads can be created.

## Default number of threads

Configuring JVM - Not recommended

`java.util.concurrent.ForkJoinPool.common.parallelism=100`

Sending the stream to a custom FJP. the reduce operation decides which thread pool the stream gets evaluated.

```java
Stream<Integer> integerParallelStream =
    list.parallelStream()
    .filter(num -> num * 1 == num)
    .map(num -> incrementWith1SecDelay(num))
    //.forEach(num -> {})
    ;

customizingForkJoinPool(integerParallelStream);//Sending the stream
```

Runs the code in the thread which resilves the reduce operation
```java
ForkJoinPool forkJoinPool = new ForkJoinPool(100);//parallelism = 100
forkJoinPool.submit(
        () -> integerStream.forEach(e -> {}));
//Running the reduction operation in another method with another thread

forkJoinPool.shutdown();
```


parallel with find first

```java
 //Find the name of the first employee greater than 40 years of age
 String empName = employees.parallelStream()
         .filter(Objects::nonNull).filter(emp -> null != emp.getAge()).filter(emp -> null != emp.getName())
         .filter(emp -> emp.getAge() > 25)
         .map(emp -> emp.getName())
         .findFirst()//Ordered and thus yields same result in both parallel and sequential
         .orElse("No Emp Found");
```

Erratic behaviour

```java
//Find the name of the any employee greater than 25 years of age
 String empName = employees.parallelStream()
         .filter(Objects::nonNull).filter(emp -> null != emp.getAge()).filter(emp -> null != emp.getName())
         .filter(emp -> emp.getAge() > 25)
         .map(emp -> emp.getName())
         .findAny()//behaves erratically with Parallel stream. Runs fine with sequential execution
         .orElse("No Emp Found");
```

## Stats

```java
 System.out.println("Available Processors : " + Runtime.getRuntime().availableProcessors());
 System.out.println("Total Memory : " + Runtime.getRuntime().totalMemory());
 System.out.println("Fork Join Pool : " + ForkJoinPool.commonPool());
```

Notice the difference between the total number of processors and parallelism in the thread pool complying
`# of threads <= # of cores`

```java
Available Processors : 16
Total Memory : 545259520
Fork Join Pool : java.util.concurrent.ForkJoinPool@659e0bfd[Running, parallelism = 15, size = 0, active = 0, running = 0, steals = 0, tasks = 0, submissions = 0]
```
