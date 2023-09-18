---
title:  "Zipkin Distributed Tracing Server"
date:   2019-11-17 23:21:00
categories: Spring Microservices
tags: [Spring Microservices]
---

# Zipkin Distributed Tracing Server

* Rabbit MQ Should be installed and run

```sh
/usr/local/sbin/rabbitmq-server
```

* Install Zipkin Distributed Tracing Server from <https://zipkin.io/pages/quickstart>

* Launch Zipkin server on <http://localhost:9411/zipkin/>


SET RABBIT_URI=amqp://localhost java -jar zipkin.jar
