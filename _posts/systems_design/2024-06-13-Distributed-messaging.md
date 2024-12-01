---
title:  "Distributed Messaging"
date:   2024-06-13 11:02:00
categories: [System Design]
tags: [System Design]
---

{% include toc title="Index" %}

> Means of loosely coupling sub-systems

[Kafka Basics](https://nitinkc.github.io/microservices/essential-kafka/)

# Messaging Protocols
- **STOMP** - Simple Text Oriented Messaging Protocol
- **MQTT** - Message Queue Telemetry Protocol (for machine to machine - IOT)
- **AMQP** - Asynchronous Messaging Queueing Protocol
  - Rabbit MQ 
  - Kafka

# Messages vs Events
In terms of OOP, Message is the Super class with Event and Command as
subclasses.

What is typically understood by message is actually a command.

## Event
- Has already happened, in the past
- **order of events can't be changed** as history can't be altered
- Can be sent via the **Event Streaming Platform** like Apache Kafka Streams
- typically represents a state change
- Events are often used to indicate that something has occurred in the system
  that other parts of the system might be interested in.

### Characteristics
- **Decoupling**: Events are usually published to an **event queue** or **an
  event stream**,
  and consumers (or subscribers) can process these events independently.
  The producer of the event doesn’t need to know who the consumers are.
- **Immutable**: Once an event is created and published, it doesn’t change.
  It’s a record(log) of something that had happened.

## Command/Message
- request for a task to be done
- order and priority can change
- Can be sent via API calls (point to point or async) or via "Message Brokers"
  like Apache Active MQ, Rabbit MQ, Solace
- typically refers to a piece of data or a command sent from one component to
  another within a system.
- Unlike events, messages often contain commands or instructions that prompt a
  specific action or response

### Characteristics
- **Direct Communication**: Messages are often used in point-to-point
  communication or request-response patterns. The sender of the message
  typically expects a specific response or action from the receiver.
- **Contextual**: Messages can include commands, requests, or data that needs to
  be acted upon.
  The sender and receiver usually have a defined relationship.

![eventVsMessage1.png](../../assets/images/eventVsMessage1.png)

![eventVsMessage2.png](../../assets/images/eventVsMessage2.png)

# Example
- Payment service creates an **event** `<<payment received>>` and published it
  to kafka event streaming platform.
- Order service subscribes to the event published and processes the payment.
- Order service, then, send a **message/command** `<<send invoice>>` to a
  messaging queue like RabbitMQ, ActiveMQ or solace.
- Communication service subscribes to the message and reads the messages and
  processes it.

![paymentProcessingArchitecture.png](../../assets/images/paymentProcessingArchitecture.png){:
width="50%" height="50%"}

# Messages
- immutable array of bytes
- topic -> feed of messages

See : Topic Partitioning

Queue helps keeping track of requests and redirect in case of a failure

- Asynchronous requests
- In a queue, data persistence

# 4 actors of Messaging
> **Producer** --> Sends message --> to an **exchange** --> Routed to --> **Queue** --> Delivered to --> a **Consumer**

### Exchanges
- Actual AMQP elements where messages are sent at first
- takes a message and routes it into one or more queues
- Routing Algo decides where to send messages from exchange
- Routing algo depends on exchange type and rules called "bindings"

# Why is kafka fast

![](https://www.youtube.com/watch?v=UNUz1-msbOM)
Kafka is optimized for high Throughput.

### Reliance of Sequential I/O

2 types of Disk Access patterns

- Random access
- Sequential access

Kafka uses **append only logs** as its primary data structure which adds new
data to the **end of the file**

HHD is 1/3 of the price, but 3 times capacity due to which kafka can keep
messages (cost effectively) over a long period of time

### Zero Copy principle
The data page is loaded from the disk to the OS buffer (RAM??) - zero copy

the directly from RAM into the NIC Buffer (kafka uses system call called
sendFile()

to tell the OS to directly copy the data from the OS cache to the network
interface card buffer)

With modern network card, this copying is done with the DMA (Direct Memory
Access) - when its used, the CPU is not involved