---
title:  "MapStruct Mapper"
date:   2023-02-21 09:16:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---

{% include toc title="Index" %}

# Introduction
MapStruct is used For converting the Entity to DTO.

Common use case is when the data is retrieved from DB and the response from the microservice 
is expected in a different format or with less or more number of fields, then map struct can be utilized for 
conversion.

```java
@Mapper
public interface EmployeeMapper {
    @Mapping(target="employeeName", source="entity.name")
    @Mapping(target="dateOfBirth", source="entity.dob")
    @Mapping(target = "phones", source = "entity.phones")
    @Mapping(target = "addresses", source = "entity.addresses")
    EmployeeDto employeeToEmployeeDto(Employee entity);//This will be implemented by MapStruct

// Target = EmployeeDto
// Source = Employee
```

<div class="container">
  <div class="row ">

    <div class="col-md-6">
        public class EmployeeDto
            private String employeeName;
            private Date dateOfBirth;
            private Map<String, String> phones;
            private List<Address> addresses;
    </div>

    <div class="col-md-6">
        @JsonProperty("name") private String name;
        @JsonProperty("dateOfBirth") private Date dob;
        @JsonProperty("phones") private Map<String, String> phones;
        @JsonProperty("addresses") private List<Address> addresses;
    </div>

  </div>
</div>

The reverse is also possible. The data from UI form or from some client, can be prepared to be inserted into DB
from DTO to DB Entity.

# Refer article

[Refer Another Article](https://nitinkc.github.io/spring/microservices/map-struct/)




