---
title:  "Jackson Mapper"
date:   2023-02-19 09:16:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---

{% include toc title="Index" %}

# Dependencies

```yaml
//Jackson Mapper
implementation group: 'com.fasterxml.jackson.core', name: 'jackson-databind', version: jacksonVersion
implementation group: 'com.fasterxml.jackson.core', name: 'jackson-annotations', version: jacksonVersion
implementation group: 'com.fasterxml.jackson.core', name: 'jackson-annotations', version: jacksonVersion
implementation group: 'com.fasterxml.jackson.core', name: 'jackson-core', version: jacksonVersion
// https://mvnrepository.com/artifact/com.fasterxml.jackson.datatype/jackson-datatype-jsr310
implementation group: 'com.fasterxml.jackson.datatype', name: 'jackson-datatype-jsr310', version: '2.17.0-rc1'
```
### Problem 
Get rid of the empty objects as pointed

![Image Text]({{ site.url }}/assets/images/jacksonMapper.png)

From jackson mapping alone, it can't be taken care of as per this blog post [https://github.com/FasterXML/jackson-databind/issues/2376](https://github.com/FasterXML/jackson-databind/issues/2376){:target="_blank"}

Suppose the return from DB (Employee Object) contains Address array list object. 

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

The class that contains List of Address is 

```java
@Builder
public class Employee {
    @JsonProperty("name")
    private String name;

    @JsonProperty("dateOfBirth")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")
    @JsonInclude(value = JsonInclude.Include.CUSTOM, valueFilter = DateOfBirthFilter.class)
    private Date dob;

    @JsonProperty("datelocaltzdt")
    @JsonDeserialize(using = LocalDateTimeDeserializer.class)
    private LocalDateTime datelocaltzdt;

    @JsonProperty("phones")
    @JsonInclude(content = JsonInclude.Include.CUSTOM, contentFilter = PhoneFilter.class)
    private Map<String, String> phones;

    @JsonProperty("addresses")
    @JsonInclude(value = JsonInclude.Include.CUSTOM, contentFilter = EmptyListFilter.class)
    //@JsonInclude(JsonInclude.Include.NON_EMPTY)
    private List<Address> addresses;
}
```

# Date Deserializer 

if the datetime column of the DB is sent as a String, 
```json5
{
  "datelocaltzdt": "2023-08-04T12:15:00"
}
```

Deserialize the properly date formatted String as LcoalDatetime class.

```java
import com.fasterxml.jackson.datatype.jsr310.deser.LocalDateTimeDeserializer;

@JsonProperty("datelocaltzdt")
@JsonDeserialize(using = LocalDateTimeDeserializer.class)
private LocalDateTime datelocaltzdt;
```

Helpful in sorting the deserialized data based on chronological order

```java
Collections.sort(data, Comparator.comparing(Employee::getDatelocaltzdt).reversed());
```
## JsonInclude

Exclude NULL or EMPTY

`@JsonInclude(JsonInclude.Include.NON_NULL)`

Exclude properties with NULL values. Include all non-null values
`@JsonInclude(JsonInclude.Include.NON_EMPTY)`

#### Emptiness
* For Collections and Maps, method isEmpty() is called;
* For Java arrays, empty arrays are ones with length of 0
* For Java Strings, length() is called, and return value of 0 indicates empty String
* and for other types, null values are excluded but other exclusions (if any).


## Custom Filter
Further filters (apart from Include.NON_NULL, NON_EMPTY etc ) can be added (typically on individual properties) using the `CUSTOM` include. 

### Class Level
If custom include filter is used at class level, it gets applied to each member (field) of the class individually, and not as a group together.

Thus, we cannot remove an Address Object if all the fields/elements of class `Address` are null. 

```java
@JsonInclude(value = JsonInclude.Include.CUSTOM, valueFilter = ClassLevelFilter.class)
public class Address {
    ...
}
```

### Field Level
We can remove individual elements using the filter criteria (or by Include.NON_NULL) and if all elements are removed, only `{}` is returned

If the custom value filter is used at the field level in Employee class, the then filter can decide whether to incluse the whole list or exclude it. The filter will be unable to 
remove the empty objects of the List. For example, if the first element of `addresses` list has all the fields as null, and if nulls are ignored in the `Address` class, the final output will be `{}`
```java
public class Employee {
    ...
    @JsonProperty("addresses")
    @JsonInclude(value = JsonInclude.Include.CUSTOM, valueFilter = EmptyListFilter.class)
    private List<Address> addresses;
    ...
}
```

### contentFilter vs valueFilter

#### Value Filter
`@JsonInclude(value = JsonInclude.Include.CUSTOM, valueFilter = DateOfBirthFilter.class)`

* Filter (to be used for determining inclusion criteria) Object specified by `JsonInclude.valueFilter()` for value itself

While performing filter, the object's equals() method is called with value to serialize.
* if equals method returns **true**   -> value is excluded (filtered out);
* if equals method returns **false**  -> value is included.


NOTE: the filter will be called for each non-null value, but handling of null value differs: {: .notice--info}
* up to Jackson 2.13, call was only made once, but 
* with 2.14 and later filter will be called once for each null value too.
{: .notice--info}

#### Content Filter

Filter 
`@JsonInclude(content = JsonInclude.Include.CUSTOM, contentFilter = PhoneFilter.class)`

* `JsonInclude.contentFilter()` is used for contents of structured types (like email format, phone number format etc)

```java
public class Employee {
    ...
    @JsonProperty("phones")
    @JsonInclude(content = JsonInclude.Include.CUSTOM, contentFilter = PhoneFilter.class)
    private Map<String, String> phones;
    ...
}
```

The phone filter uses a pattern to filter out the phone number that does not follow a particular pattern
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

## Apply formatting

`@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")`

```java
public class Employee {
    ...
    @JsonProperty("dateOfBirth")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")
    private Date dob;
    ...
```

| Input                                               | output                                              | 
|:----------------------------------------------------|:----------------------------------------------------|      
| {% gist nitinkc/14973504b39336196f505fa1c332c6de %} | {% gist nitinkc/6c804a3de35e042537bc1e7ad25e3720 %} |


## References

[https://www.javadoc.io/doc/com.fasterxml.jackson.core/jackson-annotations/latest/com/fasterxml/jackson/annotation/JsonInclude.Include.html](https://www.javadoc.io/doc/com.fasterxml.jackson.core/jackson-annotations/latest/com/fasterxml/jackson/annotation/JsonInclude.Include.html){:target="_blank"}