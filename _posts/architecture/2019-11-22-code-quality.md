---
categories: Architecture
date: 2019-12-04 21:15:00
tags:
- Code Quality
- Best Practices
- Clean Code
title: Code Quality
---

* Readability
* Maintainability
* Testability

Code coverage Tools

# Writing Testable Code

No Curly in lambdas

* Discipline to write code
* modularizing the code to smaller cohesive functions
* not to write Lambdas that are a beast
* make Lambda as a glue
  code - http://blog.agiledeveloper.com/2015/06/lambdas-are-glue-code.html
* use the test to be able to debug the code
* Write code using tests - Test first development

Use polymorphism rather than type checking - avoid instance of at all costs

//Exception handling is imperative stype of programming

//In function programmingm we deal with the stream of Data - data flow

hand it over to downstreams - flat type return car rental

reactive has error channel

handle the exception **as error** rather than exception

# Mike Cohen's Test Pyramid

- write tests with different granularity
- the higher you go up the pyramid, the fewer tests you should have
- 70% unit tests, 20% service tests, 10% UI tests

![](https://www.researchgate.net/publication/375982003/figure/fig3/AS:11431281207360823@1701189466064/The-agile-test-automation-pyramid-by-Mike-Cohn-1.jpg)


![Quality-Attributes.png]({{ site.url }}/assets/images/Quality-Attributes.png)