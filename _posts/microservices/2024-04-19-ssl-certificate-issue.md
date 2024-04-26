---
title:  "Security Certificate Issue"
date:   2024-04-19 21:00:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---

Caused by: javax.net.ssl.SSLHandshakeException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target

![sslIssueFix.png]({{ site.url }}/assets/images/sslIssueFix.png)

# Postman Settings

Turn On/Off based on the certificate
![disableSecurity.png]({{ site.url }}/assets/images/disableSecurity.png)

![sslPemFileinPostman.png](..%2F..%2Fassets%2Fimages%2FsslPemFileinPostman.png)