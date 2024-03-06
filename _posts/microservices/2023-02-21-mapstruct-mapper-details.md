---
title:  "MapStruct Mapper"
date:   2023-02-21 09:16:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}

# Introduction
MapStruct is used For converting the Entity to DTO.

DB output -> mapper/transformer/convertor -> VIEW


Common use case is when the data is retrieved from DB and the response from the microservice 
is expected in a different format or with less or more number of fields, then map struct can be utilized for 
conversion.

If DB Output is
```json
{
"first-name" : "Lorem",
"middle-name" : "k",
"last-name" : "ipsum"
}
```

and VIEW (dito/angular UI) needs the following o/p
```json
{
"fName" : "Lorem k"
"lName" : "ipsum"
}
```

[Pattern used in the example](https://www.baeldung.com/mapstruct#2-inject-spring-components-into-the-mapper)

Call a custom method defined in the `@Mapping` annotation with `qualifiedByName` attribute

OR

Create an Annotation for it --> Ref: [Custom Mapper Annotation](https://www.baeldung.com/mapstruct-custom-mapper#custom-mapper-annotation)

* target → Target DTO Class variable name
* source → Source DB Entity class variable name
* Mapping from Source DB Entity to Target DTO entity

{% gist nitinkc/e6016bf92643dcb9b44eaa124c0e6d3d %}

Implement the methods from `expression` (processName method here in the example)  or `qualifiedByName` properties (processNoData method)

{% gist nitinkc/d0fd23e897d1fd5e44a8551daa41c714 %}

# Retrieving a mapper

#### Mapper Factory
Mappers.getMapper(TestMapper.class)
* [Using The Mappers factory](https://mapstruct.org/documentation/stable/reference/html/#mappers-factory)


```java
@Mapper(componentModel = "default")//componentModel is optional for default
public interface TestMapper {
    ...
}
```

Calling Class can use the Mappers factory to retrieve the relevant object
```java
import org.mapstruct.factory.Mappers;

final TestMapper mapper = Mappers.getMapper(TestMapper.class);
```

#### Dependency Injection
@Mapper(componentModel = "spring")

* Using Dependency Injection - Spring framework

Specify the component model to which the generated mapper should adhere.

Supported values are
* default: the mapper uses no component model, instances are typically retrieved via Factory Mappers.getMapper(Class)
* spring: the generated mapper is a **Spring bean** and can be retrieved via `@Autowired`

{% gist nitinkc/dc5974e7fbb51c4d9cf6f878534bd495 %}

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

# Data Type conversion


## Applying formnatting

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


## Explicit conversion with Expressions

Converting a piece of data from one type to another

#### defaultExpression

@Mapping annotation has a defaultExpression attribute.  It determines the value of the destination field if the source field is null

```java
@Mapping(target = "extraField", source = "employee.nullTester", defaultExpression = "java(com.github.javafaker.Faker.instance().chuckNorris().fact())")
```

| Input is a null string                              | Output is a string based on Faker.instance().chuckNorris().fact() | 
|:----------------------------------------------------|:------------------------------------------------------------------|      
| {% gist nitinkc/aa3fa41108d15ebd1089010e22ba9b1b %} | {% gist nitinkc/aa316a68f721727af3e4dc9309db378f %}               |


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

The mapper can be written in such a way, that the value of the Map is mapped with the POJO it is being mapped

{% gist nitinkc/a2131a8cb4df37399d6cd58e006a1900 %}


# Refer article

[Refer Another Article](https://nitinkc.github.io/spring/microservices/map-struct/)