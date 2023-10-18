---
title:  "Reactive Programming"
date:   2022-08-06 08:30:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}

# [Reactive Manifesto](https://www.reactivemanifesto.org/)

![Diagram](https://www.reactivemanifesto.org/images/reactive-traits.svg)

Reactive Programming is equivalent to Functional programming ++

Asynchronous Programming : [vert.x library of Java](https://vertx.io/introduction-to-vertx-and-reactive/)

Three options available

* handle()
* exceptionally()
  The above two catches the exception and recovers
* whenComplete() -> Catches Exception but does not recover

## Responsive :

There should be an upper limit of response time off an application and an application should respond back to the user
within a defined time limit. Eg. For a compute intensive task

* Can design a parallel algorithm (consumes lot of resources)
* Can design async tasks ()

## Resilient

In resilient systems, deal with errors gracefully.

Eg. on DB Failures,

* Use Cache
* Use Backup db in replication sync

## Elastic

## Message Driven

Systems can achieve loose coupling. The components of the system should talk to each

other by asynchronous communication.

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
