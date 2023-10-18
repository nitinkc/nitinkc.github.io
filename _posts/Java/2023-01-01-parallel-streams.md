---
title:  "Parallel Streams"
date:   2023-01-01 18:10:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}

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

Runs the code in the thread which resolves the reduce operation
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
