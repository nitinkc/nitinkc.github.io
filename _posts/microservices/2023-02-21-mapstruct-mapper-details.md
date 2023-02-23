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

# Retrieving a mapper
* [Using The Mappers factory](https://mapstruct.org/documentation/stable/reference/html/#mappers-factory)

```java
//import TestMapper Class
import org.mapstruct.factory.Mappers;
final TestMapper mapper = Mappers.getMapper(TestMapper.class);
```
# Field Mapping
Mapping Fields With Different Field Names between Source and Target Objects

```java
@Mapper
public interface EmployeeMapper {
    @Mapping(target = "employeeName", source = "entity.name")
    @Mapping(target = "dateOfBirth", source = "entity.dob")
    @Mapping(target = "phones", source = "entity.phones")
    @Mapping(target = "addresses", source = "entity.addresses")
    EmployeeDto employeeToEmployeeDto(Employee entity);//This will be implemented by MapStruct
}
// Target = EmployeeDto , Source = Employee
```

| Employee                                            | EmployeeDto                                         | 
|:----------------------------------------------------|:----------------------------------------------------|      
| {% gist nitinkc/d867c06073103b74a39466f9a9cc2718 %} | {% gist nitinkc/f6ceaf913062d7aae7e8fff04fe09033 %} |

The reverse is also possible. The data from UI form or from some client, can be prepared to be inserted into DB
from DTO to DB Entity.


# Multiple source parameters

When the Target Object class comprises fields which is a combination of multiple objects

{% gist nitinkc/37db7c00e09ee3d2cbd499d52d40df00 %}

# Type conversion

#### dateFormat
Applying the `dateFormat` attribute

```java
@Mapping(target = "birthDate", source = "employee.dob", dateFormat = "dd-MM-yyyy HH:mm:ss")
```

| Input                        | Output                            | 
|:-----------------------------|:----------------------------------|      
| "dateOfBirth": 1676878272857 |"birthDate" : "20-02-2023 01:31:12"|

#### numberFormat
Similarly Applying the `numberFormat` attribute

```java
@Mapping(target="test", source="tester.test", numberFormat = "₹#.00")
```

| Input            | Output            | 
|:-----------------|:------------------|      
| "tester" : 52.32 | "test" : "₹52.32" |


# Expression & defaultExpression

#### defaultExpression

@Mapping annotation has a defaultExpression attribute.  It determines the value of the destination field if the source field is null

```java
@Mapping(target = "extraField", source = "employee.nullTester", defaultExpression = "java(com.github.javafaker.Faker.instance().chuckNorris().fact())")
```

```json
{
 "extraField" : "Chuck Norris can write infinite recursion functions... and have them return."
}
```

#### qualifiedByName

Use the qualifiedByName attribute of @Mapping Annotation to invoke the java method to take more control
```java
@Mapping(target = "phones", source = "employee.phones", qualifiedByName = "processPhoneMap")//Map to List

//Implement the method qualified with processPhoneMap
@Named("processPhoneMap")
List<String> processPhoneMap(Map<String, String> phoneMap) {
        ...
        //Change the Map to a List
}
```

| Input is a map of phone numbers                     | Output is a List of Strings                         | 
|:----------------------------------------------------|:----------------------------------------------------|      
| {% gist nitinkc/1702f1118e55c0512d2e04961cd281a1 %} | {% gist nitinkc/14a786fc4ce7d9e7df6c58c23c8bab34 %} |


# Mapping a Map into a Bean(Pojo)

In Case the data from JSON is not read into a JavaObject but instead into a Map using TypeReference

```java
Map<String, String> jsonAsMap = objectMapper.readValue(url, new TypeReference<Map<String, String>>() {});
TesterDto testerDto = mapper.testMapperFromMap(jsonAsMap);
```

The mapper can be written in such a way, that the value of the Map is mapped with the PJO it is being mapped

{% gist nitinkc/a2131a8cb4df37399d6cd58e006a1900 %}


# Refer article

[Refer Another Article](https://nitinkc.github.io/spring/microservices/map-struct/)