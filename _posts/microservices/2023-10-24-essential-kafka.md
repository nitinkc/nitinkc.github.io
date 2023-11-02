---
title:  "Kafka Essentials"
date:   2023-10-24 23:41:00
categories: [Microservices]
tags: [Microservices]
---

# Kafka Terminology
**Producer**: A producer is a client that sends messages to the Kafka server to the specified topic.
**Consumer**: Consumers are the recipients who receive messages from the Kafka server.
**Broker**: Brokers can create a Kafka cluster by sharing information using Zookeeper. A broker receives messages from producers and consumers fetch messages from the broker by topic, partition, and offset.
**Cluster**: Kafka is a distributed system. A Kafka cluster contains multiple brokers sharing the workload.
**Topic**: A topic is a category name to which messages are published and from which consumers can receive messages.
**Partition**: Messages published to a topic are spread across a Kafka cluster into several partitions. Each partition can be associated with a broker to allow consumers to read from a topic in parallel.
**Offset**: Offset is a pointer to the last message that Kafka has already sent to a consumer.


Kafka Message Processing
In Kafka, messages are not "queued" in the traditional sense. Instead, they are published to Kafka topics and stored in log files within Kafka brokers. Kafka uses a distributed commit log to store messages, and consumers read messages from these log files.

Here's how it works:

Producers Publish Messages: Producers send messages to Kafka topics. Kafka appends these messages to the end of the topic's log.

Messages are Retained: Messages in Kafka logs are retained for a configurable period, even after consumers have read them. This retention period is typically set by the Kafka configuration.

Consumers Read Messages: Consumers subscribe to topics and read messages from Kafka logs. They maintain an offset to keep track of which messages they have consumed.

Parallel Processing: Multiple consumers can read messages from the same topic in parallel. Each message is read by only one consumer within a consumer group.

Offset Management: Kafka keeps track of the offset (position) of each consumer within a topic. This allows consumers to resume reading from where they left off, making Kafka a distributed message processing system.

Kafka is a distributed streaming platform, designed for high-throughput, fault-tolerant, and distributed data streaming. While messages are not queued in the traditional sense, Kafka's design allows for efficient and scalable message processing.

Messages are not removed immediately after being consumed, but they will eventually be deleted based on the retention policy. The retention policy ensures that Kafka can handle large volumes of data while allowing consumers to catch up on messages they might have missed.




###
Download kafka : https://kafka.apache.org/downloads

Run the following commands 
```shell
cd /Applications/Development/kafka_2.13-3.6.0
bin/zookeeper-server-start.sh config/zookeeper.properties
```

In another tab

```shell
cd /Applications/Development/kafka_2.13-3.6.0
bin/kafka-server-start.sh config/server.properties
```

## Conduktor

https://docs.conduktor.io/gateway/


Download and install and run once the kafka server is running on local and 



## Naming convensions

{consuming system}-{kafka topic name}-{consuming service}-group

register-reg.student.engineering-hostelservice-group

