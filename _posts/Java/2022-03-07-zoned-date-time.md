---
title:  "Java ZonedDate Time"
date:   2022-03-08 00:27:00
categories: ['Java']
tags: ['Java']
---

"yyyy-MM-dd'T'HH:mm:ss.SSSZ" format would look like "2022-03-03T09:08:56.064+0000" 

As per [Java 17 documentation](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/text/SimpleDateFormat.html)

Z would format the date with timezone in the end with + or - sign indicating the timezone compared to UTC. 

RFC 822 time zone |	-0800 |

{% gist nitinkc/22f8f3ea4afcf340d49a2610407297fc %}

### ZonedDateTime
{% gist nitinkc/7e3dc6cb2ac498e478a8a1d92b3537f9 %}


### Converting from SQL Timestamp to ZonedDateTime 

Often the timestamp conversion is needed to and from DB time stamp column

```java
public static ZonedDateTime convertToZonedDateTimeFromSqlTimeStamp(Timestamp sqlTimestamp, ZoneId zoneId) {
        return Optional.ofNullable(sqlTimestamp)
        .map(time -> ZonedDateTime.ofInstant(time.toInstant(), 
                                    Optional.ofNullable(zoneId).orElse(ZoneOffset.UTC)))//if no zone offset, then use UTC by default
        .orElse(null);
}

//If no zone offset information is to be passed
public static ZonedDateTime convertToZonedDateTimeFromSqlTimeStamp(Timestamp timestamp) {
        return convertToZonedDateTimeFromSqlTimeStamp(timestamp, ZoneOffset.UTC);
}
```

### Converting from ZonedDateTime into SQL Timestamp

```java
public static Timestamp fromDate(ZonedDateTime date) {
        return Optional.of(Timestamp.valueOf(date.toLocalDateTime())).orElse(null);
}

```