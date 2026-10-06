---
title: Network Protection
date: 2026-10-05 11:02:00
categories:
- System Design
tags:
- Security
- Networking
- Zero Trust
---

{% include toc title="Index" %}

Protecting the perimeter and the pipes: DDoS, WAF, segmentation, and the
VPN→Zero-Trust evolution.

# DDoS — Distributed Denial of Service

Attackers flood you from many sources; the target is **availability**.

| Layer | Attack | Mitigation |
|-------|--------|------------|
| L3/L4 (volumetric) | UDP/SYN floods — saturate bandwidth | Anycast scrubbing (Cloudflare, Cloud Armor), provider absorbs it |
| L4 (state exhaustion) | connection-table floods | SYN cookies, conn limits |
| L7 (application) | expensive endpoints hammered ("HTTP flood") | WAF + rate limiting + autoscaling + caching |

You cannot absorb a volumetric DDoS yourself — it's an upstream bandwidth
problem; that's why scrubbing services exist. L7 attacks are your problem:
rate limits, CAPTCHAs, caching, cheap 404/401 responses.

# WAF — Web Application Firewall

Inspects L7 traffic for attack signatures (SQLi, XSS, path traversal)
before the app sees it — Cloudflare WAF, AWS WAF, ModSecurity.

- Managed rulesets (OWASP CRS) + custom rules (geo, bot, rate)
- **It's a compensating control, not the fix** — false positives happen,
  bypasses happen; patch the vuln, use the WAF for coverage/response time
- Virtual patching: block exploit of a known CVE while the fix ships

# Network Segmentation

```text
Internet ──> LB ──> public subnet ──> app subnet ──> data subnet
                        │               │               │
                   WAF/IDS        no public IPs    DB: no ingress
                                                 except app subnet
```

- Private subnets, no public IPs on backends/databases
- Firewall rules deny by default; allow only required flows
- Blast-radius control: a compromised web tier can't reach the DB
  directly without the app-tier hop
- mTLS between services so network location isn't the only check

# VPN vs Zero Trust / IAP

**Traditional perimeter model (VPN)**: authenticate once at the boundary,
then the internal network is flat and trusted — "hard shell, soft center."
Lateral movement after breach is the classic failure.

**Zero Trust model**: *never trust, always verify* — every request is
authenticated and authorized regardless of network location.

```text
VPN:       user ──> VPN gateway ──> "inside" = broad network access

Zero Trust user ──> IAP/IdP check (identity + MFA + device + policy)
    :                 ──> only the specific app/VM requested
```

Google's BeyondCorp pioneered this; **Identity-Aware Proxy (IAP)** is the
GCP implementation — per-request auth, IAM-checked, backend stays
private, no VPN needed. Full flow in
[SSO]({% post_url systems_design/security/2024-06-28-SSO %}).

Benefits: least-privilege by default, auditable per-request decisions,
works for remote workforce, blast radius is one app not the network.

# Malicious-code & supply-chain protection

- Dependency scanning (SCA), pinned versions, artifact signing
- Sandbox/egress-limit untrusted code paths
- EDR/CSPM at runtime for detection since prevention is never complete

# DRM — Digital Rights Management

Content-protection layer (licensed decryption keys + attested playback):
Widevine (Android/Chrome), **FairPlay** (Apple), PlayReady. Worth knowing
exists for streaming design; encrypting the stream ≠ controlling playback.
