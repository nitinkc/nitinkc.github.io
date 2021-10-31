---
# layout: static
title:  "Query Parameter - Special Cases"
date:   2021-10-13 21:55:00
categories: Spring Miocroservices
tags: [Spring Microservices, Spring Boot]
---

# Case 1 

```
v1/customer/{customerId}/orders?orderDate=10-11-2021
```
The difficulty is in taking the date in a particular format and parse it. Only Date is involved and not the time field.

Notice the data format and required parameter
{% gist nitinkc/eed96501e39f600a1c69969c378ba6ce %}

