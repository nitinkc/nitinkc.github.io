---
title:  "Map Struct"
date:   2023-02-14 22:50:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---


[Pattern used in the example](https://www.baeldung.com/mapstruct#2-inject-spring-components-into-the-mapper)

Call a custom method defined in the @Mapping annotation with qualifiedByName attribute

OR

Create an Annotation for it --> Ref: [Custom Mapper Annotation](https://www.baeldung.com/mapstruct-custom-mapper#custom-mapper-annotation)

* target → Target DTO Class variable name
* source → Source DB Entity class variable name
* Mapping from Source DB Entity to Target DTO entity

{% gist nitinkc/e6016bf92643dcb9b44eaa124c0e6d3d %}

Implement the methods from `expression` (processName method here in the example)  or `qualifiedByName` properties (processNoData method) 

{% gist nitinkc/d0fd23e897d1fd5e44a8551daa41c714 %}


