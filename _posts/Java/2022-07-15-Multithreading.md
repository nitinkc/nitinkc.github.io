---
# layout: static
title:  "Multithreading"
date:   2021-10-13 21:55:00
categories: ['Java']
tags: ['Java']
---

Asynchronous Task Execution Engine -> Executor Service introduced in J1.5

It has 
    * Work Queue (Blocking Queue)
    * Completion Queue
    * Thread Pool

As soon as the work is placed in the work queue, you get Future. Future is a proxy or refrence of the result that will be returned in the Future


Fork Join Framework (used in parallel stream behind the scenes) -> Java 7 (Extends Executor service)


# CompletableFuture

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

### thenCombine()
    * combines independent CompletableFutures (Async Tasks)
    * For Example : if a service makes 2 calls to independent services, then the total latency will be MAX(service1, service2) instead of SUM(service1, service2)
    * takes 2 arguments, CompletionStage and BiFunction
    * returns CompletableFuture

### thenCompose()
    * Completion Stage method
    * used for applying transform one data to another, takes a Function
    * deals with functions that **returns CompletableFuture<T>**
    * thenCompose depends on the completion of the dependent Future task



# CompletableFuture and Reactive Manifest

### Responsive
    * Asynchronous
    * Control return immediately, and the response will be collected whrn its ready
    * example CompletableFuture.supplyAsync() runs asynchronously 

### Resilent
    * No code crash on Exception or Error

### Elastic 
    * Async tasks run is a thread pool (Fork join pool)
    * # threads can go up down automatically

### Message Driven
    * Event driven async tasks interaction
    * thenAccept() runs on completion of supplyAsync(event is done and signalling to initiate thenAccept is received)

# Exception handling with Completablle Future

Three options available
    * handle()
    * exceptionally()

    The above two catches the exception and recovers 

    * whenComplete() -> Catches Exception but does not recover