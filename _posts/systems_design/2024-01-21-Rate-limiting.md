---
title:  "Rate Limiting"
date:   2024-01-21 09:30:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

Can be in an application server or a DB server or any type od servers

Overloaded systems can
- increase latency
- OOM errors
- results in cascading failures (when one fails, all requests are transferred to another overloading the other one)


**Rate Limiting Algorithms** 

# Sliding Window Rate Limiting
 Allow only a certain number of requests in a time interval. Additional requests are dropped

- Simple to implement

Issues
- Memory footprint 

If sliding window is of size N, keep N requests in the memory.

- Garbage collection

finding the requests to evict needs N searches each time


# Timer Wheel Algorithm

The timer wheel allots requests to slots based on the time of their arrival.

- Size of the wheel (Number of buckets) = Timeout of the incoming request
- Bucket is numbered 0 to Timeout -1
- Each bucket can store a limited number of requests (In a Linked List or a Queue)
- Request is added into the bucket number = **Time % Number of buckets/Size of Wheel**, Modulo operator keeps it revolving
  - System can pull requests from this queue one by one.
- Before inserting a new request into a bucket it deletes all the existing requests (These requests have not been processed by the system)


### Hierarchal Timer Wheel



# Rate Limiting Internal Requests


Ways to identify the request overloading within the system

- Average response time : if its increasing, then the system is overloaded
- Age of meggases in the wait Queue : If the Queue is slowly processed, the average age of the request in the queue will be increasing
- Increased number of requests in the Dead Letter Queue

