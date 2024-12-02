---
title:  "Cloud Native"
date:   2024-11-30 14:02:00
categories: [System Design]
tags: [System Design]
---

{% include toc title="Index" %}

[Cloud Native Landscape](https://landscape.cncf.io/?view-mode=grid)

![cloudNativeLandscape.png]({{ site.baseurl }}{% post_url /assets/images/cloudNativeLandscape.png)

# Cloud Hosting Models: 
> IaaS - CaaS - PaaS - FaaS - SaaS - Serverless

**IaaS (Infrastructure as a Service)**
- Virtualized computing resources (VMs, storage, networking)
- Users control infrastructure, provider manages physical hardware
- Example: Amazon EC2, Microsoft Azure Virtual Machines
 
**CaaS (Container as a Service)**
- Deploy, manage, and scale containerized applications
- Provider manages infrastructure and container orchestration
- Example: Google Kubernetes Engine, Amazon ECS, EKS, Fargate

**PaaS (Platform as a Service)**
- Build, deploy, and manage applications without worrying about infrastructure
- Provider manages infrastructure, servers, networking, OS, etc.
- Example: Heroku, Microsoft Azure App Service

**FaaS (Function as a Service)**
- Deploy individual functions, executed in response to events/triggers
- Provider manages infrastructure and auto-scales functions
- Example: AWS Lambda, Google Cloud Functions

**SaaS (Software as a Service)**
- Software provided over the internet, eliminating need for installation
- Provider manages infrastructure, application, and data
- Example: Salesforce, Microsoft Office 365

**Serverless**
- Cloud provider manages infrastructure and auto-scales resources
- Pay only for resources consumed
- Example: Azure Functions with Azure Cosmos DB, AWS Lambda with Amazon DynamoDB

> FaaS is a specific implementation of serverless computing

# Macroservices to Nanoservices
> Monolithic -> Modular Monolithic -> Microservices -> Nanoservices (Serverless Functions)

# Cloud-Native Pillars

![cloudNativeArchitecture.png]({{ site.baseurl }}{% post_url /assets/images/cloudNativeArchitecture.png)