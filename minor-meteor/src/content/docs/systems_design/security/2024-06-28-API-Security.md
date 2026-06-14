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

Use of HTTPS for API Communications. Provides Encrypted connection
- prevents evendropping
- man-in-the-middle attack

Use of OAuth 2.0 : Industry standard Authorization protocol

- Authorization server (like google or facebook) creates and grants permission
  to auth token
- no credentials shared, just temporary access token

# WebAuthn

facial recognition, fingerprint, flash drive

# Use Leveled API keys

use keys like readOnly, write keys, admin keys etc to provide varying levels of
authorization to various services and use cases.

- helps minimiing the blast radiius in case the key is compromised

# Implement Authorization

Role Based Access Control (RBAC)

# Rate limiting

implement rate limiting rules

# API Versioninng

# OWASP Security Risks

# API Gateway

# Error Handling

don't expose full stack trace as it can help an attacker

# Input Validations

- Avoids SQL Injection
- Cross site scripting
-