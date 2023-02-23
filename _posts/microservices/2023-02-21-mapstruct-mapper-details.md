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

```java
@Mapper
public interface PersonMapper {
    @Mapping(target = "employeeFirstName", source = "employee.name")
    @Mapping(target = "employeeLastName", source = "employee.name")
    @Mapping(target = "birthDate", source = "employee.dob")
    @Mapping(target = "phones", source = "employee.phones")//Map to List
    @Mapping(target = "beerBrand", source = "beer.brand")
    @Mapping(target = "beerName", source = "beer.name")
    @Mapping(target = "alcohol", source = "beer.alcohol")
    @Mapping(target = "carMakeAndModel", source = "vehicle.makeAndModel")
    @Mapping(target = "carColor", source = "vehicle.color")
    @Mapping(target = "driveType", source = "vehicle.driveType")
    @Mapping(target = "fuelType", source = "vehicle.fuelType")
    @Mapping(target = "specs", source = "vehicle.specs")
    @Mapping(target = "doors", source = "vehicle.doors")
    @Mapping(target = "licensePlate", source = "vehicle.licensePlate")
    PersonDto personMapper(Employee employee, Beer beer, Vehicle vehicle);
}
```

# Type conversion

Applying the `dateFormat` attribute

```java
@Mapping(target = "birthDate", source = "employee.dob", dateFormat = "dd-MM-yyyy HH:mm:ss")
```

| Input                                              | Output                                              | 
|:---------------------------------------------------|:----------------------------------------------------|      
| ```json { "dateOfBirth": 1676878272857 } ```       | ```json { "birthDate" : "20-02-2023 01:31:12" } ``` |

Similarly 

`numberFormat = "$#.00"`


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

Input is a map of phone numbers

```java
{
    "phones" : {
        "Work" : "(123) 456 7890",
        "Cell" : "987-654-3210",
        "Home" : "963-852-7410"
    }
}
```

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
Output 
```json
{
  "phones": [
    "Work:(123) 456 7890",
    "Cell:987-654-3210",
    "Home:963-852-7410"
  ]
}
```



# Refer article

[Refer Another Article](https://nitinkc.github.io/spring/microservices/map-struct/)
