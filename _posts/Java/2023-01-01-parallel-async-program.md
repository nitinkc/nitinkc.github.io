---
title:  "Parallel vs. Asynchronous Programming"
date:   2023-01-01 18:10:00
categories: ['Java']
tags: ['Java']
toc: true
---

* Both Parallel and Asynchronous tasks has threads
  * Parallel needs to join, and the slower process defines the overall speed. 
    * Eg : A pen is complete, when pen cap task, refill task and pen body task is completed
  * For Asynchronous, not waiting for completion, but when results does arrive, move on to do other things with it.
    * use the call back to receive response

Concurrency : looking for a new job, while working on the current job, during office hours.
Parallelism : maintaining 2 jobs, with 2 managers, without telling either manager
Asynchronous : 

## Parallel Streams

Martin Fowler : Collection pipeline pattern

* Imperative style has accidental complexity
  * Converting a for loop is a nighmare to convert it onto parallel program.
  * unnecessasary complexity trying to synchronize and parallelize
    * Structure of program needs to be changed
* Functional style has less complexity. The codes well explaining business logic. 
  * Easier to parallelize
  * maintainale: Structure remains the same, just parallel gets added


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
| Sequestion vs parallel                           | Synchronous vs Asynchronous                        |
| Entire pipeline is either sequential or parallel | Depends                                            |
| no segments                                      | subscribeOn - no segements \n onserveOn = segments |


## History of multithreads

Java 1 : Threads -> one set of API for all machines. hardware independent

Java 5 : ExecutorServices API -> Pool of threads 
  * Issue 1: Pool induced deadlock
  * One thread breaks the problem and throws in the pool and waits foe the result to come back
  * All the threads in pool just divided the work, and no thread left to take care of the problem

Java 7 : Fork Join pool
  * Workstealing : the threads that divides problem, also solves one of the divided part

Java 8 : uses Java 7 FJP 
  * Common Fork join pool


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

## IO intensive Problem vs Computationally intensive problem

Computationally intensive
  number of threads should be less than or equal to number of cores

For IO Intensive
   number of threads may be greater than number of cores

```math
\sqrt{3}
```
