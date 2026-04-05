---
title: Java + Kafka + SSL Interview Answers
date: 2026-04-03 00:20:00
categories:
- Java
tags:
- Interview
- Kafka
- Spring
- Security
- SSL
- Microservices
---

{% include toc title="Index" icon="cog" %}

### Asked about what logging / monitoring tools were used and about authentication and authorization handling in services?
**Logging/monitoring:** structured logs with correlation id, centralized in ELK/Splunk; metrics in Prometheus/Grafana; tracing via OpenTelemetry or Zipkin.

**AuthN/AuthZ:**
- API gateway validates JWT/OAuth2 tokens.
- Services use mTLS or OAuth2 client credentials for service-to-service calls.
- Kafka uses SASL/SCRAM or mTLS, plus ACLs per topic/group.

### Tell me about the challenge you faced in your role that was overwhelming and how did you handle it?
Example: a sudden spike in traffic caused consumer lag and cascading timeouts. I handled it by:
- Prioritizing critical flows and temporarily shedding non-critical load.
- Scaling consumer instances and increasing partitions.
- Adding backpressure and retry policies.
- Writing a postmortem with action items (capacity planning, alerts, rate limits).

### What challenges did you face in elastic search implementation?
- Mapping changes breaking queries or aggregations.
- High cardinality fields causing memory pressure.
- Index size growth and slow reindexing.
- Tuning refresh intervals and shard counts for write-heavy workloads.

### What is required to enable HTTPS?
- A server certificate (public cert or internal CA).
- Private key and a configured keystore.
- Correct TLS configuration in the server (cipher suites, protocol versions).
- Optional client truststore for mTLS.

### What are spring annotations? Explain the difference between @component and @service and when you would use them?
Spring annotations are metadata that drive dependency injection and configuration.
- `@Component` is generic and used for any bean.
- `@Service` is a specialization for service layer beans; it is semantically clearer and may enable AOP features like transactions by convention.

### What is the difference between trusted certificate and self-signed certificate?
- A trusted cert is signed by a CA that is in the trust store (public or internal CA).
- A self-signed cert is signed by itself and is untrusted unless explicitly added to a trust store.

### Explain how SSL handshake and how to configure it in a spring boot application?
**SSL handshake:** client and server negotiate TLS version and cipher, server sends its cert, client verifies trust chain, keys are exchanged, and a secure session starts.

**Spring Boot config (server side):**
```yaml
server:
  ssl:
    enabled: true
    key-store: classpath:keystore.p12
    key-store-password: changeit
    key-store-type: PKCS12
    key-alias: server
```

### Gave a use case where the server certificate is not found in the trusted store and asked what would happen and which exception would it get?
The TLS handshake fails because the client cannot validate the server certificate. Common exceptions:
- `javax.net.ssl.SSLHandshakeException: PKIX path building failed`
- Root cause often includes `sun.security.validator.ValidatorException`.

### How would you design a high-performance application to receive big load of files from a client server and ask about the major requirement (scalability) while doing so?
- Use a dedicated upload service with streaming I/O (avoid loading full files in memory).
- Store files in object storage (S3/GCS/MinIO) with multipart upload.
- Use a queue for metadata and async processing.
- Horizontal scale with stateless instances behind a load balancer.

### How would you handle fault tolerance and how would you use Kafka and distributed consumers?
- Multiple consumers in a group for parallelism and failover.
- Idempotent processing and retries with backoff.
- Use exactly-once where needed (Kafka Streams or transactional producers/consumers).
- Persist processing state with checkpoints.

### Have you used NATS.io before?
If yes: mention lightweight pub/sub for internal events and request/reply for low latency.
If no: acknowledge and compare to Kafka (NATS for low-latency messaging, Kafka for durable log and replay).

### Explain SSL Certificate and how Java/Spring handles the expired SSL Certificate.
An SSL certificate proves server identity and has a validity period. When expired:
- Java TLS rejects it during handshake (`SSLHandshakeException`).
- Fix by renewing the cert and updating the keystore/truststore.

### How Java handles millions of raw file downloading using the FTP.
- Use streaming APIs (`InputStream` to `FileChannel`) and avoid buffering whole files.
- Use a bounded thread pool for parallel downloads.
- Retry transient failures and validate checksums.

### How to ensure that each thread download only single file and does not start downloading the file that’s already in progress (downloading)
- Use a shared concurrent set or database lock keyed by file id.
- Acquire lock before download; release on completion or failure.
- Consider a work queue so each file is assigned exactly once.

### How does Kafka handle bad messages. Bad means any payload that violates standard contract.
- Validate on producer and consumer.
- Non-retryable errors go directly to DLT with reason metadata.
- Schema Registry compatibility prevents most contract violations at deploy time.

### Have you encountered a design conflict with your team. How did you manage the conflict without breaking team integrity.
Example: I asked for a short design review, listened first, proposed a time-boxed spike to compare options, and used data (latency, cost, complexity) to decide. Everyone stayed aligned because the process was transparent.

### Tell me a situation where an issue was proposed to be resolved with a different approach, but you had different idea which you have convinced your team to implement and succeeded.
Example: We planned to scale the DB vertically, but I suggested caching and query optimization. After a short POC, we improved latency 40% and avoided costly scaling.

### How java handles memory internally. How to avoid memory leaks in a large monolithic application.
Java uses heap memory managed by GC. To avoid leaks:
- Avoid static references to large objects.
- Close resources (`try-with-resources`).
- Use weak references for caches.
- Profile with heap dumps and fix object retention paths.

### In your current, what would a last suggestion you would have given to your team as a process or any technical improvements.
Example: invest in SLOs, error budgets, and automated canary releases to reduce incident risk.

### How do you dockerize a microservice? How Kubernetes helps along with docker.
- Write a small `Dockerfile`, build and tag image, push to registry.
- Kubernetes deploys containers, handles scaling, health checks, rolling updates, and config via ConfigMaps/Secrets.

### Java Questions on multithreading, concurrent collections, file transfers, security etc.
Quick points to cover:
- Thread safety: `synchronized`, `Lock`, `volatile`, and `Atomic*` classes.
- Concurrent collections: `ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`.
- File transfers: streaming, backpressure, checksums, retry policy.
- Security: TLS, OAuth2/JWT, input validation, least privilege, secret rotation.

