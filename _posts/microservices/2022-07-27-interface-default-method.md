---
# layout: static
title:  "Default method in Interface"
date:   2022-07-27 13:06:00
categories: "Spring Microservices"
tags: [Java, Interfaces]
---
{% include toc title="Index" %}

# Context
The major advantage of a default method in an Interface comes into play in this scenario. 

Need a convertor that can convert or map one Object type into another. Often the data returned from DB needs to be mapped with business objects and it could be a list of objects or a single object. To accomodate both types (Single object or a list of object), the default method in the interface can be written like this :-

### Defining the Interface
{% gist nitinkc/83007b76b4afc24ca39761195af2de35 %}

Lets take an example of the implementation. On the implementation side, developer has to focus on just converting one object into another and the rest gets taken care of by default method

### Implementing the interface
For all tyopes od tables in the DB, same concerter can be used by defining the individual converters by overriding the convert method.
{% gist nitinkc/f5149ff2a6dacd72b24732c5f52dfc94 %}

The interface can be used to convert an entire list
```java
@Autowired
MyConvertor myConverter;
...
...
List<Data> dataList = someRepo.findAll();
List<DataDto> dataDtoList =  myConverter.convert(dataList);
```

or the same can used to convert just one object
```java
Data data = someRepo.findById('someId');//returns one row
DataDto dataDto =  myConverter.convert(dataList);
```