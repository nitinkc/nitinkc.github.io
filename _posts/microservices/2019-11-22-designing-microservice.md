---
title:  "Designing a microservice"
date:   2019-11-22 21:35:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---

All Microservices Projects are hosted in

https://github.com/spring-microservices-learning

[Details of the Projects and revision projects](https://github.com/microservices-revisions/initial-download)

| Application                       | Repository                                                                                |
|-----------------------------------|-------------------------------------------------------------------------------------------|
| 1. Limits Service                 | git clone https://github.com/spring-microservices-learning/limits-service.git             |
| 2. Spring cloud Config Server     | git clone https://github.com/spring-microservices-learning/spring-cloud-config-server.git |
| 3. Global Config Repository       | git clone https://github.com/spring-microservices-learning/config-repo.git                |
| 4. Currency Exchange Microservice | git clone https://github.com/spring-microservices-learning/currency-exchange.git          
| 5. Currency Converter             | git clone https://github.com/spring-microservices-learning/currency-exchange.git          |


## URLs

| Application                                  | URL                                                                                                                                                                                      |
|----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Limits Service                               | http://localhost:8080/limits                                                                                                                                                             |
| Spring Cloud Config Server                   | http://localhost:8888/limits-service/default http://localhost:8888/limits-service/dev                                                                                                    |
| Currency Converter Service - Direct Call     | http://localhost:8100/currency-converter/from/USD/to/INR//usr/local/var/log/rabbitmq/rabbit@localhost.log/usr/local/var/log/rabbitmq/rabbit@localhost.logquantity/10                     |
| Currency Converter Service - Feign           | http://localhost:8100/currency-converter-feign/from/EUR/to/INR/quantity/10000                                                                                                            |
| Currency Exchange Service                    | http://localhost:8000/currency-exchange/from/EUR/to/INR http://localhost:8001/currency-exchange/from/USD/to/INR                                                                          |
| Eureka                                       | http://localhost:8761/                                                                                                                                                                   |
| Zuul - Currency Exchange & Exchange Services | http://localhost:8765/currency-exchange-service/currency-exchange/from/EUR/to/INR http://localhost:8765/currency-conversion-service/currency-converter-feign/from/USD/to/INR/quantity/10 |

## VM Argument to run multiple instances of a microservice
`Dserver.port=8001`

## Ports

| Application                       | Port                  |
|-----------------------------------|-----------------------|
| Limits Service                    | 8080, 8081, ...       |
| Spring Cloud Config Server        | 8888                  |
|                                   |                       |
| Currency Exchange Service         | 8000, 8001, 8002, ..  |
| Currency Conversion Service       | 8100, 8101, 8102, ... |
| Netflix Eureka Naming Server      | 8761                  |
| Netflix Zuul API Gateway Server   | 8765                  |
| Zipkin Distributed Tracing Server | 9411                  |

