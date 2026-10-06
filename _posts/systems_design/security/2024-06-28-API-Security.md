---
title: API Security
date: 2024-06-28 11:02:00
categories:
- System Design
tags:
- Security
- API
- Authentication
- Best Practices
---

{% include toc title="Index" %}

Layered defenses for public-facing APIs, roughly in the order a request
hits them.

# Use HTTPS for all API communications

Encrypted connection via TLS — prevents eavesdropping and
man-in-the-middle attacks. Enforce HSTS; redirect or flatly reject HTTP.
See [HTTPS]({% post_url systems_design/security/2024-06-28-HTTPS %}).

# Authentication & Authorization

## OAuth 2.0

Industry-standard authorization protocol:

- The authorization server (Google, Okta, PingFederate) grants a
  scoped access token — credentials are never shared with the API consumer
- Validate `exp`, `iss`, `aud`, signature on every request
  ([JWT details]({% post_url systems_design/security/2026-10-05-Sessions-Tokens-JWT %}))
- Check authorization **per request per resource** — a valid token for
  user A must not fetch user B's data (BOLA, below)

## WebAuthn

Phishing-resistant auth for browser-facing flows — facial recognition,
fingerprint, security keys. See
[Authentication Mechanisms]({% post_url systems_design/security/2024-06-28-Authentication-mechanisms %}).

## Leveled API keys

Issue keys with distinct privileges — `readOnly`, `write`, `admin` —
tailored to each service/use case.

- Minimizes **blast radius** if a key leaks
- Treat keys as secrets: never in URLs (they land in logs), client-side
  code, or git. Rotate on a schedule, support instant revocation.
- For internal service-to-service calls prefer mTLS or signed JWTs over
  long-lived keys.

## Authorization model

Role-Based Access Control (RBAC) for most APIs; ABAC/ReBAC when context
or relationships matter. See
[Authorization Models]({% post_url systems_design/security/2026-10-05-Authorization-models %}).

# Rate limiting

Throttle requests per key/IP/user to stop abuse, brute force, credential
stuffing, and cost amplification.

- Return `429` + `Retry-After`; use sliding window/token bucket
- Stricter limits on expensive and auth endpoints (`/login`, `/reset`)
- Details: [Rate Limiting]({% post_url systems_design/security/2024-01-21-Rate-limiting %})

# API Versioning

`/v1/` prefixes let you evolve (and patch/deprecate) without breaking
clients — and let you force-stricter rules on old versions. Deprecate
versions with known weaknesses; don't keep them alive forever.

# API Gateway

A single ingress that centralizes the cross-cutting checks so each
service doesn't reimplement them:

```text
Client ──> WAF ──> API Gateway ──> Services
                   ├─ TLS termination
                   ├─ AuthN token validation (JWT/mTLS)
                   ├─ Rate limiting / quotas
                   ├─ Request schema validation
                   └─ Logging / audit
```

See [API Gateway]({% post_url systems_design/security/2024-06-14-API-Gateway %}).

# Input Validation

Validate everything the client sends — allowlist, don't blocklist.

- **Parameterized queries / ORM only** — avoids SQL injection
- **Encode output by context** — avoids cross-site scripting
- Enforce schema (types, lengths, ranges) at the edge; reject unknown fields
- Never trust client-supplied IDs/roles — derive identity from the token,
  not the request body
- Cap request sizes to prevent resource exhaustion

# Error Handling

- Return generic errors to clients (`400 invalid request`, `500`)
- Never expose stack traces, framework versions, SQL errors, or internal
  hostnames — each is reconnaissance for an attacker
- Log the full error server-side with a correlation ID, and return only
  that ID to the client

# OWASP API Security Top 10 (key items)

1. **BOLA** — Broken Object Level Authorization: `/users/123/orders/456`
   must verify the caller owns object 456. The #1 API vuln.
2. **Broken Authentication** — weak token validation, no rate limits on login
3. **Broken Object Property Level Auth** — mass assignment: filtering
   what you *return* vs what the caller may *see/mutate*
4. **Unrestricted Resource Consumption** — no limits → cost/DoS
5. **Broken Function Level Auth** — admin endpoints reachable by users
6. SSRF, security misconfiguration, injection, unsafe third-party consumption

# Audit & Monitoring

- Log auth failures, authz denials, rate-limit hits, validation errors
- Alert on anomaly patterns (bulk record reads, geographic impossibilities)
- Correlation IDs end-to-end for forensic reconstruction
