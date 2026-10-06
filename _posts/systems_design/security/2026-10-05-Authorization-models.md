---
title: Authorization Models
date: 2026-10-05 11:02:00
categories:
- System Design
tags:
- Security
- Authorization
- RBAC
---

{% include toc title="Index" %}

Authentication answers "who are you"; authorization answers "what may you
do." Models differ in how the permission decision is expressed and
evaluated.

# ACL — Access Control List

Per-object lists of who can do what. Together they form the **access
control matrix** of the system.

```text
              read  write  delete
file.txt      nitin  nitin  admin
report.pdf    team   admin  admin
```

- Granularity: user-based, role-based, resource-based, group-based
- Simple and intuitive per-resource ("who can see this doc?")
- Doesn't scale for broad questions ("what can this user access across
  1M resources?") and matrix grows O(users × resources)
- Real-world: Unix file permissions, GCP/AWS IAM *bindings* on resources

# RBAC — Role-Based Access Control

Permissions attach to **roles**; users get roles.

```text
user ──> role ──> permissions
nitin ──> "sre-oncall" ──> {read:logs, restart:service}
      └─> "viewer"     ──> {read:dashboard}
```

- Easy to administer: change the role, not every user
- Standard in enterprises and IAM (roles like `roles/editor`)
- **Explodes** ("role explosion") when permissions don't map cleanly —
  hundreds of near-duplicate roles; can't express context ("only my own
  records", "only during business hours")

# ABAC — Attribute-Based Access Control

Decisions are computed from **attributes** of the subject, resource,
action, and environment via policies:

```text
allow if  user.dept == resource.dept
      and user.clearance >= resource.sensitivity
      and request.time within business_hours
```

- Extremely expressive — context, time, device posture, data labels
- Harder to audit: "who can access X" requires evaluating policies, not
  reading a list
- Real-world: AWS IAM conditions, GCP IAM Conditions, XACML

# ReBAC — Relationship-Based Access Control

Permissions derive from **relationships in a graph**: "you can edit a doc
if you own it, belong to its team, or it was shared with you."

- Models Google Drive / Zanzibar-style sharing naturally
- Real-world: Google Zanzibar, OpenFGA, SpiceDB
- Right fit for social/collaborative products; overkill for simple apps

# Policy Engines / Rule Engines

Decouple the *decision* from the app: the app asks "is this allowed?" and
an engine evaluates declarative rules.

- **OPA / Rego** — general-purpose policy engine (K8s admission, APIs)
- **Cedar** (AWS) — readable policy language, formal analysis
- **OpenFGA / SpiceDB** — ReBAC-as-a-service

```text
App ──> "can user U do action A on resource R?" ──> Policy Engine ──> allow/deny
```

Benefits: consistent enforcement, auditability, testable policy-as-code,
no permission logic scattered through code.

# DAC vs MAC (interview trivia)

- **DAC** (discretionary) — the resource *owner* grants access (Unix files,
  Google Drive sharing)
- **MAC** (mandatory) — the *system* enforces clearance levels; owners
  can't override (SELinux, military "top secret" models)

# Design guidance

- Default **deny**; grant explicitly
- **Least privilege** — minimum permissions, minimum duration
  (just-in-time elevation beats standing admin)
- Check authorization **server-side on every request** — never trust
  hidden UI buttons or unvalidated IDs (that's IDOR/broken access control,
  the #1 OWASP API risk)
- Centralize: middleware/mesh/policy engine, not per-endpoint ifs
- Log authorization denials — they're your best attack signal
