---
title:  "Spring Boot Revisions"
date:   2023-09-15 11:50:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
toc: true
---

# Stereotype Annotations

@Component, @Controller, @Service, and @Repository 

# GET Request

`@RequestMapping(method = RequestMethod.GET)` OR
`@GetMapping("/student/{studentId}")`

Read the Path Variable 
`@PathVariable` in the method parameter

```java
@GetMapping("/student/{studentId}")
public ResponseEntity<Student> getStudentById(@PathVariable Long studentId) {
    return ResponseEntity.ok(studentService.getStudentById(userId));
}
```

### Map model to Response and add return validation

### Add Validation to the Request



# POST Request

`@RequestMapping(method = RequestMethod.POST)` OR
`@PostMapping("/students")`

Read the Request Body 
`@RequestBody` in the method parameter

[Link title]({{ site.baseurl }}{% post_url 2021-02-13-POST-Requests %})

