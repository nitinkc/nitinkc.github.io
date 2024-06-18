---
title:  "API Protocols"
date:   2024-05-22 11:02:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

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

(https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#rest-api-vs-graphql)(https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#rest-api-vs-graphql)

![](https://www.youtube.com/watch?v=yWzKJPw_VzM)

# Webhooks
- Custom HTTP Callbacks triggered by specific events
- eliminated the need of polling 

# SOAP

# Web socket
- persistent, low latency bi-directional data exchange
- facilitate realtime data exchange
- ideal for applications where instant updates are critical, like chat applications, online gaming, trading platforms

# gRPC

Modern, high-performance, Protocol Buffers

Suitable for microservices architectures 


