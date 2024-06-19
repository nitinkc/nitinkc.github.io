---
title:  "API Protocols"
date:   2024-05-22 11:02:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}


[https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#communication-protocols](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#communication-protocols)

# REST API

Top pick for Web API's
- Simple
- Scalable and works well with web services 
- standard HTTP Methods
- Stateless so scaling up easily achieved
- Over fetching data issue
- to get related data, multiple network calls, thus increasing latency


# GraphQL
 UI can ask the precise data and its sent in one go
 - strongly types schema & precised data retrieval
 - supports realtime updates through subscriptions
 - But, the flexibility can overwhelm the backend
 - since its dynamic, caching is trickier

[https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#rest-api-vs-graphql](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#rest-api-vs-graphql)


![](https://www.youtube.com/watch?v=yWzKJPw_VzM)



# Webhooks
Webhooks are a powerful way to enable real-time communication between systems. 

They allow one system to send automated notifications or data updates to another system when certain events occur, 
without the need for the receiving system to continually check (constant polling) for updates.

- reverse APIs or push APIs because the server sends HTTP requests to the client 

[https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#what-is-a-webhook](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#what-is-a-webhook)

- Custom HTTP Callbacks triggered by specific events
- eliminated the need of polling 

![](https://www.youtube.com/watch?v=x_jjhcDrISk)


# Web socket
- persistent, low latency bi-directional data exchange
- facilitate realtime data exchange
- ideal for applications where instant updates are critical, like chat applications, online gaming, trading platforms


# gRPC

Modern, high-performance, Protocol Buffers

Suitable for microservices architectures 

[https://nitinkc.github.io//system%20design/gRPC-RPC/](https://nitinkc.github.io//system%20design/gRPC-RPC/)

# SOAP


