---
title: Passwords in DB
date: 2024-06-13 11:02:00
categories:
- System Design
tags:
- Security
- Database
---

{% include toc title="Index" %}

![](https://www.youtube.com/watch?v=zt8Cocdy15c)

# OWASP guidelines for storing Passwords into the DB

[OWASP guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

**Never store plaintext or reversibly-encrypted passwords.** Store a
slow, salted, one-way hash.

### One-way Password **Hashing** Algorithm

- Deliberately slow — discourages brute-force attacks
- MD5, SHA-1, even SHA-256 are **too fast** for passwords — billions of
  guesses/sec on a GPU; do not use them for password storage
- Vulnerable to pre-computation attacks:
  - rainbow tables
  - database-based lookups

### Adding Salt to the Password

Salt: unique, randomly generated string **per password**.

`Hash(password + Salt)` → ensures the hash is unique to each password,
even for identical passwords across users.

- Makes pre-computation attacks (rainbow tables) unattractive — the
  attacker must recompute per user
- Salt is **not secret** — store it next to the hash

Password matching:

```text
DB columns: [ salt | hash ]

Login:
  salt          = fetch(user)
  candidateHash = Hash(inputPassword + salt)
  allow         = constantTimeCompare(candidateHash, storedHash)
```

### Pepper (optional extra layer)

A pepper is like a salt but **secret and shared** across all passwords —
stored in a KMS/HSM/env var, not the DB. If only the DB leaks, hashes are
still uncrackable without the pepper. Cost: rotation complexity.

`Hash(password + salt + pepper)`

# Which algorithm?

| Algorithm | Status | Notes |
|-----------|--------|-------|
| **argon2id** | Recommended | Memory-hard; resists GPU/ASIC cracking. OWASP top pick |
| **bcrypt** | Good | Battle-tested, widely supported. `cost` factor ~10–14 |
| **scrypt** | Good | Memory-hard like argon2 |
| **PBKDF2** | Acceptable (legacy/FIPS) | Needs high iteration count (600k+) |
| MD5, SHA-1, SHA-256 | Never | Fast hashes — brute-forceable |

Memory-hardness matters because GPUs/ASICs are limited by memory bandwidth
more than compute. Tune work factors so verification takes ~250–500 ms.

# Attacks beyond brute force

- **Credential stuffing** — try breached username/password pairs from other
  sites. Defenses: MFA, breached-password denylists (e.g., k-anonymity
  checks against HaveIBeenPwned), rate limiting, CAPTCHA on failures.
- **Password spraying** — one common password across many accounts.
  Defenses: lockout/throttling per IP *and* per account, common-password denylist.
- **Phishing** — hash strength is irrelevant if the user types the password
  into a fake site. Defense: WebAuthn/passkeys (phishing-resistant),
  see [Authentication Mechanisms]({% post_url systems_design/security/2024-06-28-Authentication-mechanisms %}).

# Login-flow checklist

- Constant-time comparison of hashes (timing-safe compare)
- Generic error on failure ("invalid credentials") — don't reveal whether
  the username exists
- Rate limit login endpoints; exponential backoff / temporary lockout
- Never log passwords — not even "for debugging"
- Force re-auth (or MFA) for sensitive ops: password change, email change,
  payouts
