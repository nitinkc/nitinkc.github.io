---
title:  "Rest Template"
date:   2023-01-31 03:53:00
categories: [Microservices]
tags: [Microservices]
---

{% include toc title="Index" %}


```java
ResponseEntity<WordResponse[]> response = 
        restTemplate.getForEntity(URL, WordResponse[].class, uriVariables);
```
For POST method with `ParameterizedTypeReference`

```java
// Create parameterized type reference for Map<String, Object>
ParameterizedTypeReference<Map<String, Object>> responseType = new ParameterizedTypeReference<Map<String, Object>>() {};

// Send the POST request to the server
ResponseEntity<Map<String, Object>> responseEntity = restTemplate.exchange(URL, HttpMethod.POST,
        requestEntity,responseType);

```