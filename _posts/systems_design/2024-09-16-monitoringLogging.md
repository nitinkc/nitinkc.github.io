---
categories:
- System Design
date: 2024-09-16 14:02:00
tags:
- Monitoring
- Logging
- Observability
- Metrics
title: Monitoring & Logging
---

{% include toc title="Index" %}

# Service Layer Monitoring

- tells if the microservice is working
- Achieved via Health Endpoints(/health), Or
- By Collecting time Series Data - Telemetry(Prometheus (Timeseries DB) &
  Grafana)

# Semantic Monitoring

- monitor from business transaction, or semantic perspective
- Ex. How well the transaction performed when Customer uses it
- Achieved via Functional Testing

# Continuous Monitoring

- aka Continuous Control Monitoring
- Automated process that allows engineers to detect compliance and security
  threats
- Helps identify and track key risks in real time because it used automation