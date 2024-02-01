---
title:  "Serialization"
date:   2022-08-03 18:16:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}


To serialize an object means to convert its state to a byte stream. this byte stream can be saved to disk or can be transferred over an internet

“Serializable” means converting an instance of a class (an object) into a format where it can be written to disk, or transmitted over a network.

“Deserialization” is opposite – reading data from the disk or from network and convert into a Java object(POJO).

Implement a class with Serializable interface (A marker interface). The class will automatically be serialized and deserialized by the different serializers.

Any object reference contains within the class to be serialized, must also implkement serializable


> Serializable interface is a marker interface

Use transient to skip the variable or reference from serializable.

Static class members will also be ignored

maintaining SUID: auto SUID is generated with the instance and methods info. If changed, the SUID changes.
also auto is dangerous as you may get different SUI+D from JDK8 on windows and Open JDK 6 on linux


```java
//The transient variable does not participate in the serialization process
transient int age = 5;// If used, it takes default values upon deserialization
transient String test = "TESTING";
transient char c = '%';

//Testing final transient. Final overpowers and thus there is no effect of transient
final transient String ftString = "Final Transient String showing";

    //Similarly there is no effect of static transient
    static transient String stString = "Static Transient String showing";


    //Testing for the Static variable. Static variables are NOT The part of Object,
    //The are the part of Class
    static int staticInt = 342324;
```