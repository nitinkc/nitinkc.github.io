---
title:  "Asynchronous Programming"
date:   2023-01-03 02:30:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}

Non Blocking : when you make a method call, you dont have to wait for it to 
complete

CallBack
* CallBack lacks consistency
* Really hard to compose call backs
* hard to deal with error

Promise
    * resolve, reject or pending state
    * 2 channels -> data channel & error channel

# Railway Track pattern
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

{% gist nitinkc/17229c16e91766fa9eb903cad63a8def %}


| Current State | Next State | Function called            |
|:--------------|:-----------|:---------------------------|
| resolved      | resolved   | next then in the pipeline  | 
| resolved      | rejected   | next catch in the pipeline |
| rejected      | resolved   | next then in the pipeline  |
| rejected      | resolved   | next catch in the pipeline |

* treat error as another form of data and errors as first class citizens

> Reactive Streams has three channels, includes completed channel along with data and error tracks

From Promises, only 0 or one data, Reactive Streams has 1 or many data

Stream
    dataflow

> Exceptions and Functional programming are mutually exclusive

* CompletablFutures in Java are the Promises in Javascript

### Stages of Completable futures

When one stage completes, another one starts and it keeps running

##### thenApply()

* Completion Stage method
* used for applying transformations, takes a Function
* thenApply deals with **Function that returns** a value
* returns CompletableFuture&lt;T>() of TypeT

Promises in Java are Thenable objects thus `thenAccept()` method

##### thenCombine()
* used to combine Independent Completable Futures
* Takes two arguments  
  * CompletionStage, 
  * BiFunction
* Returns a CompletableFuture  

##### thenCompose()

* Completion Stage method
* Transform data from one form to another
* Input is a `Function` functional interface
* Deals with methods that return completableFuture

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