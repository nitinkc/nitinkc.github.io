---
title: Cryptography Basics
date: 2026-10-05 11:02:00
categories:
- System Design
tags:
- Security
- Encryption
---

{% include toc title="Index" %}

The five primitives that everything else (TLS, JWT, passwords, signatures)
is assembled from. You don't need the math — you need to know which tool
solves which problem.

# The Toolbox

| Primitive | Answers | Examples |
|-----------|---------|----------|
| Symmetric encryption | Confidentiality (fast, shared key) | AES-256-GCM, ChaCha20 |
| Asymmetric encryption | Confidentiality + key exchange without a shared secret | RSA, ECC |
| Hashing | Integrity, fingerprinting, password storage | SHA-256, bcrypt, argon2 |
| MAC / HMAC | Integrity + authenticity with a shared key | HMAC-SHA256 |
| Digital signature | Integrity + authenticity + non-repudiation | RSA-Sig, ECDSA, Ed25519 |

# Encoding ≠ Encryption ≠ Hashing

- **Encoding** (Base64, hex) — reversible by anyone, no key. Provides
  *zero* security. Base64 in a JWT is readable by anyone.
- **Hashing** — one-way. `SHA-256(x)` is fast to compute, infeasible to
  invert. Same input → same output → good for fingerprints and integrity,
  bad for passwords on its own (see rainbow tables in
  [Passwords]({% post_url systems_design/security/2024-06-13-Passwords %})).
- **Encryption** — reversible *only with the key*. This is what gives
  confidentiality.

# Symmetric Encryption

One shared secret key encrypts and decrypts.

```text
Alice ──encrypt(key, plaintext)──> ciphertext ──decrypt(key)──> Bob
```

- Very fast (~GB/s) — used for bulk data: TLS record layer, disk
  encryption, database encryption at rest
- Modern standard: **AES-256-GCM** (AEAD — gives confidentiality *and*
  integrity in one operation; never use AES-CBC/ECB for new designs)
- **The hard problem is key distribution** — how do Alice and Bob get the
  same key without an eavesdropper copying it? Solved by asymmetric crypto.

# Asymmetric (Public-Key) Encryption

A key *pair*: the public key is published; the private key is kept secret.

```text
encrypt(publicKey, msg)  ──> only privateKey can decrypt   (confidentiality)
sign(privateKey, msg)    ──> anyone with publicKey verifies (authenticity)
```

- Slow — so in practice it's used only for small payloads: exchanging
  symmetric session keys (TLS handshake) and signing.
- **RSA** — older, larger keys (2048–4096 bits); still ubiquitous in certs
- **ECC** (Elliptic Curve) — same security with much smaller keys
  (P-256 ≈ RSA-3072); preferred for new systems
- **Diffie–Hellman / ECDH** — key *agreement*: both sides derive the same
  shared secret over an insecure channel without transmitting it. Ephemeral
  DH ("DHE/ECDHE") gives **forward secrecy**: recording traffic now and
  stealing the server key later does not decrypt old sessions.

# MAC / HMAC

A keyed hash: `tag = HMAC(secretKey, message)`.

- Proves the message wasn't tampered with **and** came from someone holding
  the key
- Both sides need the shared key → no non-repudiation (either party could
  have produced it)
- Used for: API request signing (AWS SigV4), webhook verification
  (Stripe/GitHub signatures), cookie integrity

# Digital Signatures

`sig = sign(privateKey, hash(message))`; anyone verifies with the public key.

- Only the private-key holder could have produced it → **non-repudiation**
- The basis of JWTs (`RS256`/`ES256` algorithms), SAML assertions, code
  signing, and the entire certificate system below

```text
MAC      : shared key   ── "someone with the key sent this"
Signature: private key  ── "*this specific party* signed this"
```

# PKI & Certificates

If anyone can publish a public key, how do you know `api.example.com`'s key
is really theirs? **Certificates** — a Certificate Authority (CA) signs a
statement binding a public key to an identity.

```text
Browser trusts Root CA (pre-installed)
        │  Root CA signs ──>
        ▼
Intermediate CA
        │  Intermediate signs ──>
        ▼
Leaf cert for api.example.com  (public key + hostname + expiry + signature)
```

- The **chain of trust**: client verifies leaf ← intermediate ← root
- The CA never sees your private key — you generate the pair, send a CSR
  (Certificate Signing Request), get back the signed cert
- **Revocation**: CRL / OCSP / short-lived certs (Let's Encrypt = 90 days)
- This same "sign a public key" idea powers SSH `known_hosts`, JWT JWKS
  endpoints, and mTLS client certs.

# Putting It Together — the TLS pattern

Nearly every secure protocol uses the same composition:

1. **Asymmetric crypto** (handshake) — authenticate the server via its
   certificate and agree on a fresh symmetric session key (ECDHE)
2. **Symmetric crypto** (record layer) — encrypt all bulk traffic with
   AES-GCM for speed
3. **Hashing/MAC** — integrity on every message

Details in [HTTPS]({% post_url systems_design/security/2024-06-28-HTTPS %}).

# Practical Rules

- Hash passwords with **bcrypt / scrypt / argon2** — never raw SHA
- Never invent your own algorithm or protocol; use TLS, JWT libs, Tink/libsodium
- Rotate keys; design for key compromise, not just prevention
- Store keys in a KMS/HSM/Vault — never in code or config files
  (see [Secrets Management]({% post_url systems_design/security/2026-10-05-Secrets-Management %}))
- Don't encrypt without authenticating — use AEAD modes or Encrypt-then-MAC
