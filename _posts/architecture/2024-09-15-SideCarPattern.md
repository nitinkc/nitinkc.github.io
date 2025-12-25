---
title: Sidecar Pattern
date: 2024-09-15 20:02:00
categories:
- Architecture
tags:
- Microservices
- Design Patterns
- Kubernetes
---

{% include toc title="Index" %}

Deploying components of an application or service into a separate process or
container to provide isolation and encapsulation.

Main microservices focus on the core functionality

Main microservice has a "side-car" microservice for

- Logging
- Config
- Proxy to remote services etc.