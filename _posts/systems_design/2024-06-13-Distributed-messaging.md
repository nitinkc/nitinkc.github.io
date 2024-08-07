---
title:  "Kafka - Messaging Queues"
date:   2024-06-13 11:02:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

Means of loosely coupling sub-systems

Messages consumed by subscribers and created by one or more producers

Message are organized into topics. Producers put messages into topic.

Processed by Broker (Kafka, RabbitMQ)

persistent over short term.

### Messages
immutable array of bytes

topic -> feed of messages

See : Topic Partitioning

Queue helps keeping track of requests and redirect in case of a failure

- Asynchronous requests
- In a queue, data persistence

## AMQP - Asynchronous Messaging Queuing Processes
- Rabbit MQ,Kafka

# Messaging Protocols

- STOMP - Simple Text Oriented Messaging Protocol
- MQTT - Message Queue Telemetry Protocol (for machine to machine - IOT)
- AMQP - Asynchronous Messaging Queueing Protocol 

Rabbit MQ is the implementation of AMQP - Supports clustering and fault tolerance

# 4 actors of Messaging 

Producer --> Sends message --> to am exchange --> Routed to --> Queue --> Delivered to --> a Consumer

### Exchanges 
Actual AMQP elements where messages are sent at first

takes a message and routes it into one or more queues

Routing Alge decides where to send messages from exchange

Routing algo depends on exchange type and rules called "bindings"


# Why is kafka fast
![](https://www.youtube.com/watch?v=UNUz1-msbOM)
Kafka is optimized for high Throughput. 

# Reliance of Sequential I/O

2 types of Disk Access patterns
Random access
Sequential access

Kafka uses append only logs as its primary data structure which adds new data to the end of the file

HHD is 1/3 of the price, but 3 times capacity due to which kafka can keep messages (cost effectively) over a long period of time

# Zero Copy principle


The data page is loaded from the disk to the OS buffer (RAM??) - zero copy

the directly from RAM into the NIC Buffer (kafka uses system call called sendFile() 
to tell the OS to direct;y copy the data from the OS cache to the network interface card buffer)

With modern network card, this copying is done with the DMA (Direct Memory Access) - when its used, the CPU is not involved
