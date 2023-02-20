---
title:  "Jackson Mapper"
date:   2023-02-19 09:16:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---

### Problem 

![Image Text]({{ site.url }}/assets/images/jacksonMapper.png)

In order to get rid of the empty objects as pointed above

From jackson mapping alone, it can't be taken care of as per this blog post [https://github.com/FasterXML/jackson-databind/issues/2376](https://github.com/FasterXML/jackson-databind/issues/2376)

Suppose the return from DB contains Address array list object. 

{% gist nitinkc/e784b244949deab7102d7df72ab0a48e %}

The first element has all fields as null,
which appears as `{ }` in the resultant JSON output if `@JsonInclude(JsonInclude.Include.NON_NULL)` annotation is used at class level

```java
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Address {
    private String addressLine1;
    private String addressLine2;
    private String city;
    private String state;
    private String zip;
}
```

The parent class

```java
@Builder
public class Employee {
    @JsonProperty("name")
    private String name;
    @JsonProperty("dateOfBirth")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")
    @JsonInclude(value = JsonInclude.Include.CUSTOM, valueFilter = DateOfBirthFilter.class)
    private Date dob;
    @JsonProperty("phones")
    @JsonInclude(content = JsonInclude.Include.CUSTOM, contentFilter = PhoneFilter.class)
    private Map<String, String> phones;
    @JsonProperty("addresses")
    @JsonInclude(value = JsonInclude.Include.CUSTOM, contentFilter = EmptyListFilter.class)
    private List<Address> addresses;
}
```

Further filters can be added (typically on individual properties) using the `CUSTOM` include

`@JsonInclude(content = JsonInclude.Include.CUSTOM, contentFilter = PhoneFilter.class)`

```java
public class PhoneFilter {
    private static Pattern phonePattern = Pattern.compile("\\d{3}-\\d{3}-\\d{4}");//111-111-1111

    @Override
    public boolean equals(Object obj) {
        if (null == obj || !(obj instanceof String)) {
            return false;
        }
        //phone number must match the pattern 111-111-1111
        return !phonePattern.matcher(obj.toString()).matches();
    }
}
```

Difference between `contentFilter` and `valueFilter`

### Apply formatting
`@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")`

### JsonInclude

`@JsonInclude(JsonInclude.Include.NON_NULL)`

Exclude properties with NULL values. Include all non-null values

`@JsonInclude(JsonInclude.Include.NON_EMPTY)`

Exclude NULL or EMPTY

Emptiness 
  * For Collections and Maps, method isEmpty() is called;
  * For Java arrays, empty arrays are ones with length of 0
  * For Java Strings, length() is called, and return value of 0 indicates empty String
  * and for other types, null values are excluded but other exclusions (if any).


`@JsonInclude(value = JsonInclude.Include.CUSTOM, valueFilter = DateOfBirthFilter.class)`

* Filter (to be used for determining inclusion criteria) Object specified by `JsonInclude.valueFilter()` for value itself
* and/or `JsonInclude.contentFilter()` for contents of structured types (like email format, phone number format etc)

While performing filter, the object's equals(value) method is called with value to serialize.
 * if equals method returns **true**   -> value is excluded (filtered out); 
 * if equals method returns **false**  -> value is included.


NOTE: the filter will be called for each non-null value, but handling of null value differs: up to Jackson 2.13, 
call was only made once, but with 2.14 and later filter will be called once for each null value too.

## References

[https://www.javadoc.io/doc/com.fasterxml.jackson.core/jackson-annotations/latest/com/fasterxml/jackson/annotation/JsonInclude.Include.html](https://www.javadoc.io/doc/com.fasterxml.jackson.core/jackson-annotations/latest/com/fasterxml/jackson/annotation/JsonInclude.Include.html){:target="_blank"}