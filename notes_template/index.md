# Microservices Architecture: Interview Prep Guide

> **Goal:** Broad, systematic coverage — from design thinking to production deployment.
> Built for senior developers moving into architecture roles.

---

## The Mental Model: Design → Build → Run

```mermaid
graph LR
    A[Foundations] --> B[DDD]
    B --> C[Patterns]
    C --> D[Events]
    D --> E[APIs]
    E --> F[Resilience]
    F --> G[Observability]
    G --> H[Security]
    H --> I[Deployment]
    I --> J[Interview]
```

---

## Sections at a Glance

| # | Section                     | Core Topics                                                             |
|---|:----------------------------|:------------------------------------------------------------------------|
| [01](01-foundations.md) | Architectural Foundations   | Styles, CAP, Conway's Law, Hexagonal, Onion, Clean                      |
| [02](02-ddd.md) | Domain-Driven Design        | Bounded Contexts, Aggregates, Context Mapping, Ubiquitous Language      |
| [03](03-microservices-patterns.md) | Microservices Patterns      | Decomposition, Integration, Service Discovery, Caching, Sidecar, Outbox |
| [04](04-event-driven.md) | Event-Driven Architecture   | Kafka, CQRS, Event Sourcing, Saga, Messaging Patterns, DLQ              |
| [05](05-api-communication.md) | API & Communication         | REST, gRPC, GraphQL, API Gateway, BFF, Versioning, Configuration        |
| [06](06-resilience.md) | Resilience & Reliability    | Circuit Breaker, Retry, Bulkhead, Timeout, Rate Limiting, Chaos         |
| [07](07-observability.md) | Observability               | Logs, Metrics, Traces, SLO, OpenTelemetry, DORA Metrics                 |
| [08](08-security.md) | Security                    | OAuth2, JWT, mTLS, Secrets, Zero Trust, Testing Strategies              |
| [09](09-deployment.md) | Deployment & Infrastructure | Kubernetes, Helm, GitOps, Blue-Green, Canary, Configuration             |
| [10](10-interview.md) | Interview Prep              | Design scenarios, Trade-offs, ADRs, Spring Boot map                     |

---

## Recommended Reading Order

1. **Sections 01–02** — Architecture thinking + DDD (the *why* behind service boundaries)
2. **Sections 03–04** — Patterns + events (the *how* of building distributed systems)
3. **Sections 05–09** — Verify and fill gaps in what you already know
4. **Section 10** — Final synthesis through the interview lens

---

## What Architecture Interviews Actually Test

- Can you **decompose** a system into coherent services? (DDD)
- Do you understand **distributed system trade-offs**? (CAP, eventual consistency)
- Can you reason about **failure scenarios**? (Resilience patterns)
- Do you know how to **observe** a running system? (Observability)
- Can you articulate **why** you'd choose one pattern over another?

!!! tip "Breadth first, depth on demand"
    This guide is intentionally wide. If a concept feels shallow, that's your signal to go deeper on that specific topic after building the mental map.
