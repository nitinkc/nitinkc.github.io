---
title:  "Power Mock Tests"
date:   2023-11-24 03:53:00
categories: [Microservices]
tags: [Microservices]
---
{% include toc title="Index" %}

# PowerMock with Junit 4

PowerMock is a testing library that 
- extends other mocking libraries like Mockito and EasyMock.
- provides more powerful capabilities, such as mocking static methods, final classes, and private methods

With Junit 3+ Static methods can be tested with
```java
MockedStatic mocked = mockStatic(Foo.class))
```

JUnit5 and Powermockito are a big NO. There is no documentation for the combination.
We have to stick with JUnit4.
{: .notice--danger}


