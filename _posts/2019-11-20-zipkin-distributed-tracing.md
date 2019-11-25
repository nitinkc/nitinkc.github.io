---
layout: post
title:  "Zipkin Distributed Tracing Server"
date:   2019-11-17 23:21:00
categories: Spring Miocroservices
comments: true
disqus_identifier: A7655498-AB9E-40BF-A0D5-E5C6DE6BBF28
tags: [Spring Microservices, Spring Boot, Zipkin Distributed Tracing Server]
---

# Zipkin Distributed Tracing Server

* Rabbit MQ Should be installed and run
```sh
/usr/local/sbin/rabbitmq-server
```
* Install Zipkin Distributed Tracing Server from
<https://zipkin.io/pages/quickstart>
* Launch Zipkin server on
<http://localhost:9411/zipkin/>


SET RABBIT_URI=amqp://localhost java -jar zipkin.jar
