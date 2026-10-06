---
title: Sessions, Tokens & JWT
date: 2026-10-05 11:02:00
categories:
- System Design
tags:
- Security
- Authentication
- JWT
---

{% include toc title="Index" %}

How a server remembers *who* you are across requests — the two dominant
models, JWT internals, and the hard parts (theft, revocation).

# Stateful Sessions

After login the server creates a session record and hands the client a
random **session ID** (opaque, meaningless string) in a cookie.

```text
Browser                          Server
  |── POST /login (user/pass) ────>|
  |                                |── sessionStore["abc123"] = {user: nitin}
  |<── Set-Cookie: sid=abc123 ─────|
  |── GET /api/me (cookie) ───────>|
  |                                |── lookup sid ──> user
```

- Session state lives server-side (Redis, DB, memory)
- **Revocation is trivial** — delete the record, user is logged out
- Scales worse: every request needs the session store; shared state across
  replicas requires Redis/DB or sticky sessions
- Cookie risk: **CSRF** — the browser attaches cookies automatically to
  cross-site requests. Mitigate with `SameSite=Lax/Strict`, CSRF tokens.

## Cookie hardening flags

- `HttpOnly` — JS can't read it (blocks XSS token theft)
- `Secure` — HTTPS only
- `SameSite=Lax/Strict` — limits cross-site sending (CSRF)
- Short expiry + rotation on privilege changes

# Stateless Tokens

The server generates a self-contained token (signed with public/private
keys) after verifying user/password. The token itself carries the user's
identity and permissions — no server-side lookup needed.

- Server stores nothing → horizontally scalable, ideal for microservices
  and APIs (especially `Authorization: Bearer` for non-browser clients)
- **Limitation**: does not protect against **replay attacks / token theft** —
  anyone holding the token is the user (copied from devtools, Postman, logs)
- Mitigations: short TTL (`exp`), refresh tokens, mTLS binding,
  storing access tokens in memory rather than localStorage

# JWT Anatomy

`header.payload.signature` — three Base64URL parts joined by dots.

```json
header : {"alg": "RS256", "typ": "JWT", "kid": "key-1"}
payload: {"sub": "user-42", "iss": "auth.example.com",
          "aud": "api", "exp": 1759700000, "scope": "read"}
```

- **Payload is only Base64 — NOT encrypted.** Anyone can read it. Never put
  secrets/PII in claims.
- **Signature** (`RS256`/`ES256`) proves authenticity: the server verifies
  with the issuer's public key, fetched from a **JWKS endpoint**
  (`/.well-known/jwks.json`), keyed by `kid` for rotation.
- Standard claims: `iss` (issuer), `sub` (subject), `aud` (audience),
  `exp`/`iat`/`nbf` (times), `scope`, custom claims.

## Verification checklist (server side)

1. Signature valid against JWKS key
2. `exp` not expired, `nbf` valid
3. `iss` and `aud` match expected values
4. Algorithm allowlist — never accept `alg: none` or let the token choose
   between HS256/RS256 (classic algorithm-confusion attack)

# Access Token + Refresh Token pattern

```text
Login ──> access token (15 min, JWT, sent on every API call)
      └──> refresh token (days–weeks, stored more safely,
           used ONLY at the /refresh endpoint)

access expires ──> POST /refresh ──> new access (+ rotated refresh)
```

- Short-lived access token bounds the damage of theft
- **Refresh token rotation**: each use issues a new refresh token and
  invalidates the old — if an old token is replayed, the family is revoked
  (theft detection)

# The Revocation Problem

Stateless tokens can't be "deleted" — they stay valid until `exp`. Options:

- **Short TTL** — simplest; limit blast radius to minutes
- **Refresh-token revocation** — access tokens die quickly on their own;
  kill the refresh token to prevent renewal
- **Denylist/blocklist** — check a revoked-token set per request (adds back
  the lookup you were avoiding; keep it in Redis)
- **Token version / `auth_time` claim** — bump a per-user version on
  password change/logout-all; reject older tokens
- Hybrid: stateless JWT for reads, stateful check for sensitive ops

# Where to store tokens (browser)

| Storage | XSS risk | CSRF risk |
|---------|----------|-----------|
| `HttpOnly` cookie | can't be read by JS | needs CSRF protection |
| `localStorage` | any XSS = token theft | none (not auto-sent) |
| In-memory JS var | smaller window | none |

Rule of thumb: `HttpOnly Secure SameSite` cookie for browser apps;
`Authorization: Bearer` header with in-memory storage for SPAs calling
APIs; never localStorage for sensitive tokens.

**Next:** [OAuth 2.0]({% post_url systems_design/security/2024-06-28-OAuth2 %}) —
the standard way these tokens get issued by a dedicated server.
