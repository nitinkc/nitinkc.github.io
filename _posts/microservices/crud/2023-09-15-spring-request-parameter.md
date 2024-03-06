---
# layout: static
title:  "Spring Path variable & Request Parameter"
date:   2023-09-15 20:04:00
categories: "Spring Microservices"
tags: ["Spring Microservices", Spring Boot]
---


### Path variable

http://localhost:8089/api/v0/hello-world/pathVariable/{var_name}
{: .notice--info}

Read the Path Variable with `@PathVariable` in the method parameter. `@PathVariables` annotation is used to extract values from the URI path

```java
@GetMapping(path = "/pathVariable/{var_name}")
public String helloWorldPathVariable(@PathVariable("var_name") String name) {
    return String.format("The Value returned is %s", name);
}

@GetMapping("/student/{studentId}")
public ResponseEntity<Student> getStudentById(@PathVariable Long studentId) {
    return ResponseEntity.ok(studentService.getStudentById(userId));
}
```

### RequestParam

/jpa/students/pagination?page_size=5&offset=1&sortBy=email
{: .notice--info}

Check the `required` and `defaultValue` arguments of RequestParam Annotation

```java
// Retrieve all users page by page
@GetMapping(path = "/students/pagination")
public List<Student> retrieveAllUsersPagination(
        @RequestParam(defaultValue = "0") Integer offset,
        @RequestParam(value = "page_size",required = false, defaultValue = "10") Integer pageSize,
        @RequestParam(defaultValue = "id") String sortBy) {
        ...
}
```

### defaultValue with GET request

If Requirement for the API is to get the summary of recent orders in the last 24 hours (without any request params)
```
localhost:8084/orders/dashboard/summary
```

**OR** 

pass a specific date to search
```
localhost:8084/orders/dashboard/summary?fromDate=2021-06-01&toDate=2022-06-17
```

Notice the `defaultValue` property of `@RequestParam`. This is useful when the dates are not passed.
<br>
The `fromDate` param takes the **current date** as default date `#{T(java.time.LocalDateTime).now()}` 
<br>
`toDate` parameter takes **the end of the day today** as the default vale(`#{T(java.time.LocalDateTime).now().plusDays(1)}`)

{% gist nitinkc/a3d6bc27b88b20abe0eb491f107930a0 %}

If, however, explicit dates are passed and particular type of Order is also passed in request parameter

```
localhost:8084/orders/dashboard/details?fromDate=2021-06-01&toDate=2022-06-17&orderType=Grocery Order
```

{% gist nitinkc/d347e24dc5a08d8195cd86c5a32505be %}


# Case : Date without time 

```
v1/customer/{customerId}/orders?orderDate=10-11-2021
```

The difficulty is in taking the date in a particular format and parse it.
Only Date is involved and not the time field.

Notice the data format and required parameter
{% gist nitinkc/eed96501e39f600a1c69969c378ba6ce %}

