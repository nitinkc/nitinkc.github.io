---
title:  "Map Struct"
date:   2023-02-14 22:50:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---


Pattern used : https://www.baeldung.com/mapstruct#2-inject-spring-components-into-the-mapper

Either call the custom method by typing it inside the @Mapping annotation's qualifiedByName attribute
or create an ANNOTATION for it --> NOT USED IN PROJECT -> Ref: https://www.baeldung.com/mapstruct-custom-mapper#custom-mapper-annotation


* target → Target DTO Class variable name
* source → Source DB Entity class variable name
* Mapping from Source DB Entity to Target DTO entity

{% gist nitinkc/e6016bf92643dcb9b44eaa124c0e6d3d %}


{% gist nitinkc/d0fd23e897d1fd5e44a8551daa41c714 %}


