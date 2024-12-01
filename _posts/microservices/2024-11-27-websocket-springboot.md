---
title:  "SpringBoot WebSockets"
date:   2024-11-27 15:00:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---


`@EnableWebSocketMessageBroker`:

This is used for implementing a **STOMP-based messaging system.**
Suitable for applications needing a publish/subscribe model or complex routing with destinations.
Relies on Spring's simp messaging (simple messaging protocol) abstraction.
Example use case: A chat application with topic-based subscriptions.

`@EnableWebSocket`:

This is for creating raw WebSocket handlers.
Allows handling low-level WebSocket frames (e.g., TextMessage, BinaryMessage) directly.
Example use case: Custom WebSocket-based protocols or real-time data streams like stock prices.