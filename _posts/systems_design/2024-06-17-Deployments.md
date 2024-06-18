---
title: "types of deployments"
date: 2024-06-17 11:02:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

# Blue-Green Deployments

Never let the user see downtime
- if 10 servers serving, 5 deployment happening, 5 still serving

# Hot deployment

Redirect the traffic from load balancers or a proxy srvice to one env and deploy on another

# Rollback strategy

Jenkins job opr script, if the service are up ort running

