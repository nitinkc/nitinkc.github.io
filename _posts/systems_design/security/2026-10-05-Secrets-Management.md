---
title: Secrets Management
date: 2026-10-05 11:02:00
categories:
- System Design
tags:
- Security
- Secrets
- Operations
---

{% include toc title="Index" %}

Passwords for machines — API keys, DB credentials, private keys, tokens —
are the most commonly breached artifact. This is how mature systems
handle them.

# The rules

- **Never in code or git.** Scan repos (gitleaks, trufflehog) and block
  in CI/pre-commit.
- **Never in logs.** Not even "once for debugging" — logs are the first
  thing attackers read and the last thing anyone audits.
- **Never long-lived if avoidable.** Prefer short-lived, identity-based
  credentials over stored secrets entirely.
- **Always rotatable.** Design so rotation doesn't require downtime or a
  deploy — overlap old/new validity windows.
- **Access is audited and least-privilege.** Every read of a secret is
  logged; humans get secrets only via break-glass.

# The tools

| Tool | What it does |
|------|--------------|
| **Secret stores** (Vault, AWS/GCP Secret Manager, CyberArk) | Encrypted, access-controlled, audited storage + APIs to fetch secrets at runtime |
| **KMS** (cloud key management) | Manages encryption keys; keys never leave the service — you call encrypt/decrypt |
| **HSM** | Hardware root of trust — keys generated and used inside tamper-resistant hardware; the backing for KMS |
| **Privileged access** (CyberArk) | Human/admin credential vaulting, session recording, just-in-time elevation |

# Envelope encryption

The standard pattern for encrypting data at rest:

```text
Data Key (DEK) ──encrypts──> your data
   │
   └─ encrypted itself (wrapped) by a ──> Key Encryption Key (KEK) in KMS
   │
   stored alongside the ciphertext ──> decrypt DEK via KMS API when needed
```

Why: rotating the KEK only requires re-wrapping the small DEK, not
re-encrypting terabytes of data; the master key never leaves the KMS/HSM.
This is how cloud-managed disks, databases, and Vault itself work.

# Eliminating secrets instead of storing them

The modern trend: replace stored credentials with **federated workload
identity**.

- **Workload Identity / instance metadata** — a GCP/AWS service account
  identity is attested by the platform; the workload gets a short-lived
  token, no key file at all
- **OIDC federation in CI/CD** — GitHub Actions gets a short-lived cloud
  token via OIDC instead of a stored service-account key
- **Short-lived certs** (mTLS, SSH CA) — credential expires in minutes;
  theft yields almost nothing

```text
Old:  app has a static key file ──> forever valid ──> leak = incident
New:  platform attests workload ──> mints 15-min token ──> leak ≈ useless
```

# Rotation & break-glass

- Automate rotation (secrets engines rotate DB creds on lease expiry)
- Two-version rotation: deploy new, wait for propagation, retire old
- Break-glass: emergency-access secrets sealed behind approval + alerting,
  exercised periodically so they actually work when needed

# Interview checklist

Be ready to say where each secret in your design lives, how it's rotated,
who can read it, and what happens when it leaks — "it's in an env var"
is the answer that fails.
