---
title:  "Testing Estimations"
date:   2024-04-23 21:00:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}

# Unit test Estimation

based on cyclomatic complexity as per sonarcube - if the cyclomatic complexity = 2679
* There are 2679 edges in the execution graph. Theoretically, at least one test case each node is needed. 
* Meaning a minimum of 2679 test cases should be needed.

## Use of Cyclomatic Complexity:

* Determining the independent path executions thus proven to be very helpful for Developers and Testers.
* It can make sure that every path have been tested at least once.
* Thus help to focus more on uncovered paths. Code coverage can be improved.