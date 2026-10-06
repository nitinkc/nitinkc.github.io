---
title: Security Fundamentals
date: 2026-10-05 11:02:00
categories:
- System Design
tags:
- Security
- Best Practices
---

{% include toc title="Index" %}

The vocabulary and mental models every other security article builds on.

# The CIA Triad

Security goals are usually expressed as three properties:

- **Confidentiality** — only authorized parties can read the data
  (encryption, access control)
- **Integrity** — data cannot be modified without detection
  (hashes, MACs, digital signatures)
- **Availability** — the system stays usable for legitimate users
  (redundancy, DDoS protection, rate limiting)

A fourth property often added in practice:

- **Authenticity / Non-repudiation** — you can prove who did what
  (signatures, audit logs)

# Authentication vs Authorization vs Audit

The most commonly confused trio in system design:

```text
Authentication (AuthN)  ── Who are you?
                          Password, MFA, certificate, token

Authorization   (AuthZ) ── What are you allowed to do?
                          Roles, ACLs, policies, scopes

Audit / Accounting      ── What did you do?
                          Logs, trails, non-repudiation
```

- AuthN always precedes AuthZ — you cannot authorize an unidentified party.
- OAuth 2.0 is an **authorization** protocol; OpenID Connect adds the
  **authentication** layer on top of it.
- Audit is what makes the first two enforceable after the fact — without logs,
  breaches are invisible.

# Threat Modeling

Before picking mechanisms, decide what you are defending against. A lightweight
process:

1. **Identify assets** — what is valuable? (PII, credentials, money, uptime)
2. **Identify actors** — external attacker, malicious insider, compromised
   dependency, accidental misuse
3. **Enumerate trust boundaries** — every place data crosses a boundary
   (client→server, service→service, service→DB, third-party calls) is an
   attack surface
4. **List attack vectors per boundary** — a common checklist is STRIDE:

| STRIDE | Threat | Violates | Example |
|--------|--------|----------|---------|
| **S**poofing | Pretending to be someone else | Authentication | Stolen session token |
| **T**ampering | Modifying data | Integrity | Altering API payload |
| **R**epudiation | Denying an action | Audit | "I never made that trade" |
| **I**nfo disclosure | Leaking data | Confidentiality | Stack traces, verbose errors |
| **D**enial of service | Making system unavailable | Availability | DDoS, resource exhaustion |
| **E**levation of privilege | Gaining more rights | Authorization | User → admin via bug |

5. **Prioritize by risk** — likelihood × impact. You cannot defend everything;
   secure the highest-risk paths first.

# Defense in Depth

Never rely on a single control. Layer them so one failure isn't fatal:

```text
Perimeter      ── WAF, DDoS protection, TLS everywhere
Network        ── segmentation, private subnets, no public DBs
Identity       ── SSO + MFA, short-lived tokens, mTLS for services
Application    ── input validation, output encoding, authz checks per request
Data           ── encryption at rest, field-level encryption for PII, backups
Operations     ── secrets management, audit logs, alerting, patching
```

Key corollaries:

- **Assume breach** — design as if the perimeter is already compromised
  (this is the core idea behind Zero Trust).
- **Fail closed** — when a security check errors out, deny by default,
  never allow.

# Core Principles

- **Least privilege** — every identity gets the minimum access needed,
  for the minimum time. Applies to users, services, and API keys.
- **Separation of duties** — no single actor should be able to both
  request and approve a sensitive action.
- **Security by design** — retrofitting security is 10–100× more expensive;
  include it in design docs, not just pentests.
- **Don't roll your own crypto** — use vetted libraries and protocols.
  Novel schemes are almost always weaker than they look.
- **Obscurity is not security** — secret algorithms and hidden URLs are not
  controls. Assume the attacker knows the system design.
- **Shift left, verify right** — catch issues in code review/CI, but keep
  runtime monitoring because real attackers don't read your design doc.

# Common Mistakes (interview checklist)

- Treating authentication as authorization ("logged in" ≠ "allowed")
- Putting secrets in code, URLs, or logs
- Trusting client-supplied identity (user IDs in request bodies/headers)
- Exposing stack traces / verbose errors to clients
- Encrypting but not authenticating (ciphertext can still be tampered)
- Long-lived credentials with no rotation or revocation path

**Next in series:** [Cryptography Basics]({% post_url systems_design/security/2026-10-05-Cryptography-basics %})
