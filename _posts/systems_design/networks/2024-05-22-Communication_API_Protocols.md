---
title:  "API Communication Protocols"
date:   2024-05-22 11:02:00
categories: [System Design]
tags: [System Design]
---

{% include toc title="Index" %}

# Communication Standards:
[https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#communication-protocols](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#communication-protocols)

# SOAP 
XML Based for enterprise applications 

# REST API
Resource based for web servers
- Top pick for Web API's
- Built on top of HTTP using standard HTTP Methods
- Simple
- Scalable and works well with web services
- **Stateless** so scaling up is easily achieved (require each request to contain all of the information
  necessary for the server to authenticate it)
- **Over-fetching** data is an issue
- to get related data, multiple network calls, thus increasing **latency**
- Requests are cacheable

# GraphQL
we can request the specific attributes. So it saves bandwidth and also
provides security 

UI can ask the precise data and it's sent in one go
- no over-fetching or under-fetching
- - steep learning curve
- strongly typed schema & precised data retrieval
- supports realtime updates through subscriptions
- But, the flexibility can overwhelm the backend
- since its dynamic, caching is trickier

[https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#rest-api-vs-graphql](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#rest-api-vs-graphql)

![](https://www.youtube.com/watch?v=yWzKJPw_VzM)

# gRPC
- Uses Protocol Buffers
- High performance for microservices
- is generally used by microservices to communicate **internally**.
- It is written over HTTP 2.0

Suitable for microservices architectures

[https://nitinkc.github.io//system%20design/gRPC-RPC/](https://nitinkc.github.io//system%20design/gRPC-RPC/)

Thrift

Thrift has a code generator which generates data structures that can be
serialized using Thrift,
and client and server stubs for RPC, in different languages.

# Webhooks

# Web socket - persistent bidirectional full duplex connections

[https://nitinkc.github.io/system%20design/websockets/](https://nitinkc.github.io/system%20design/websockets/)


# Head-of-Line Blocking in HTTP
Head-Of-Line blocking occurs when the message/data packet at the head of the
queue cannot move forward due to congestion
even if other messages/packets behind this one could

HTTP 2.0 solves this problem using Multiplexing.
It implements multiplexing by breaking the messages/data packets into frames and
are sent in streams.

Each stream has a stream ID. So,when you get a message of a stream ID, that
stream is going to be blocked until all the
messages having the stream IDs are processed.

HTTP 2.0 solved Head of Line Blocking, but it is still written over TCP. Even
though data packets are broken into
logical streams, they are not independent because they are running on the same
TCP

# Protocols for video transmission
HTTP is not good for video transmission because:Videos are broken into chunks.
Since HTTP is stateless, the client has
to specify which chunk it wants because the server does not know about the
previous requests.

HTTP is written over TCP which is not optimal for live streaming. Because in
live streaming, if the video packet does
not reach the client then there is no point in retrying because the data is
old.So UDP is better for live-streaming.

However, in some cases where we need, guaranteed delivery TCP is preferred.

##### HTTP-DASH

DASH stands for Dynamic Adaptive Streaming over HTTPThis protocol runs over TCP.
So there is guaranteed delivery and ordering.

The basic idea is, that the client sends a signal to the main server based on
the data you can handle

In Mac devices,
HLS [HTTP live streaming](https://www.cloudflare.com/learning/video/what-is-http-live-streaming/)
is used.
It is very similar to HTTP-DASH

##### Web-RTC

WebRTC uses peer-to-peer communication . HTTP 2.0, HTTP-DASH and QUIC (HTTP 3.0)
used client-server communication

How does peer-to-peer communication work?

First, the clients get the addresses of the other clients from the server.
Then the server sends the information to both the clients.
Clients use this information to connect.

Since it does not require a serverIt is fast.It saves bandwidth.

It is more robust because even if the server crashes, clients can keep talking
to each other.
