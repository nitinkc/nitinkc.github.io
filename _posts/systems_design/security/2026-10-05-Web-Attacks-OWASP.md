---
title: Web Attacks & OWASP Top 10
date: 2026-10-05 11:02:00
categories:
- System Design
tags:
- Security
- OWASP
- Web
---

{% include toc title="Index" %}

The attack classes every web/API engineer must recognize — mapped to
OWASP Top 10 categories — with the defenses that actually work.

# Injection (SQLi, command injection)

Untrusted input is concatenated into an interpreter (SQL, shell, LDAP,
template engine).

```text
WHERE name = ' <input> '     input = ' OR '1'='1   ──> matches everything
```

- **Defense: parameterized queries/prepared statements — always.**
  ORMs default to safe; raw string-built SQL is the bug.
- Secondary: input allowlisting, least-privileged DB user (read-only
  where possible), WAF as a speed bump not the fix.

# XSS — Cross-Site Scripting

Attacker's JS executes in a victim's browser under your origin — steals
sessions, defaces, acts as the user.

- **Stored** — payload saved in DB (comment, profile), served to everyone
- **Reflected** — payload bounced off a URL/search param
- **DOM-based** — client JS writes untrusted data into `innerHTML`

Defenses:

1. **Context-aware output encoding** (HTML vs attribute vs JS vs URL)
2. Framework auto-escaping (React/Angular) — beware `dangerouslySetInnerHTML`
3. **Content-Security-Policy** header — restricts script sources
4. `HttpOnly` cookies — XSS can't read session cookie even if it fires

# CSRF — Cross-Site Request Forgery

The browser auto-attaches cookies to *any* request to your domain —
including forged ones from a malicious page.

```text
victim visits evil.com ──> <img src="bank.com/transfer?to=attacker&amt=500">
                           browser sends bank.com cookies ──> transfer executes
```

Defenses: `SameSite=Lax/Strict` cookies, anti-CSRF tokens (synchronizer
pattern), `Origin`/`Referer` checks, re-auth for sensitive ops.
Bearer-token APIs (no cookies) are immune by construction.

# Broken Access Control — OWASP #1

- **IDOR/BOLA** — `GET /invoices/{id}` returns anyone's invoice because
  the handler never checks ownership. Fix: server-side authz per object,
  per request.
- **Function-level** — admin endpoints "hidden" but reachable; UI hiding
  is not a control.
- **Mass assignment** — `POST /user` accepting a `role` field the client
  shouldn't set. Fix: explicit field allowlists / DTOs.

# SSRF — Server-Side Request Forgery

You accept a URL from the client and fetch it server-side — attacker
points it at `http://169.254.169.254/metadata` (cloud credentials) or
internal services.

Defenses: URL allowlists, resolve-then-pin DNS (blocks rebinding), block
private IP ranges, metadata service protections (IMDSv2), egress
firewalls.

# The rest of the Top 10 (2021)

| Category | Gist | Core defense |
|----------|------|--------------|
| Cryptographic failures | sensitive data in cleartext/weak algo | TLS everywhere, AES-GCM, KMS-managed keys |
| Insecure design | no threat modeling, flawed flows | design review, abuse cases (see [Fundamentals]({% post_url systems_design/security/2026-10-05-Security-Fundamentals %})) |
| Security misconfiguration | defaults, open buckets, debug on | IaC scanning, hardened baselines |
| Vulnerable components | known-CVE dependencies | SCA scanning, dependabot, patching SLAs |
| AuthN failures | weak recovery, stuffing | MFA, rate limits, breached-password checks |
| Integrity failures | unsigned updates, untrusted CI/CD | signed artifacts, SLSA/supply-chain controls |
| Logging failures | blind to breaches | structured audit logs, alerting |
| SSRF | above | egress controls |

# Verification helpers

- **CAPTCHA / reCAPTCHA / Turnstile** — raises the cost of automation
  (credential stuffing, scraping, fake signups). Friction trade-off —
  apply to risky actions, not every request.
- **Rate limiting** — foundational mitigant for most automated attacks;
  see [Rate Limiting]({% post_url systems_design/security/2024-01-21-Rate-limiting %})
- **Security headers** — `CSP`, `X-Content-Type-Options: nosniff`,
  `X-Frame-Options`/frame-ancestors (clickjacking), `Referrer-Policy`

# Interview checklist

For any user-facing endpoint, be ready to answer: how is input validated,
how is access checked per object, what happens on error, what's logged,
and what's the rate limit?
