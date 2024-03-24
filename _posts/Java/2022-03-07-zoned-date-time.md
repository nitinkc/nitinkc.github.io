---
title:  "Java ZonedDate Time"
date:   2022-03-08 00:27:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}

**Current Formatted Date, from the server running JVM, using ZonedDateTime**
```java
String formattedCurrentTimeStamp = ZonedDateTime.now()
        .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS a z(O)"));
//2024-03-23 23:14:34.984 PM MDT(GMT-6)
```

**Convert from UTC to EST/EDT**
- First convert the Input String into ZonedDateTime using parse
- Manipulate the zoneDateTime object
- Convert the zonedDateTimeObject into the Output String using the required format

[Difference between Parse and Format](https://nitinkc.github.io/algorithms/Drills/#difference-between-parse-and-format)

```java
//Convert the input time to city timeZone ()
ZonedDateTime zdtBasedOnCity = zonedDateTimeInUtc.withZoneSameInstant(ZoneId.of(cityTimeZone));

//Or
zdtBasedOnCity = zonedDateTime
        .with(LocalTime.MAX)
        .withZoneSameInstant(ZoneId.of(ZoneOffset.UTC.getId()))
        .truncatedTo(ChronoUnit.MILLIS);
```
{% gist nitinkc/ee92e4e37a323bfe0785a5c3ce4f628e %}

```java
String inputDateTimePattern = "yyyy-MM-dd HH:mm:ssX"; //"yyyy-MM-dd HH:mm:ss.SSSSSSX";
String outputDateTimeFormat = "MM/dd/yyyy HH:mm z";
String toTimeZone = "America/New_York";

String startTime = "2024-03-10 04:00:00+00"; // Start time in GMT
String endTime = "2024-03-10 07:00:00+00";   // End time in GMT

//03/09/2024 23:00 EST
System.out.println(getFormattedOutputDateTimeString
        (startTime,inputDateTimePattern, outputDateTimeFormat, toTimeZone));

//03/10/2024 03:00 EDT
System.out.println(getFormattedOutputDateTimeString
        (endTime, inputDateTimePattern, outputDateTimeFormat,toTimeZone ));
```

# Modern Java Date Time Calendar Library

From `java.time` package

The `LocalDateTime` class represents a date and time without a time zone,
while the `ZonedDateTime` class represents a date and time with a time zone.

* ZonedDateTime : A date-time with a time-zone in the ISO-8601 calendar system, 
eg. `2007-12-03T10:15:30+01:00 Europe/Paris}`.

**When would you use OffsetDateTime instead of ZonedDateTime?** 

If you are writing complex software that models its own rules for date and time calculations based on geographic locations, 
or if you are storing time-stamps in a database that track only absolute offsets from Greenwich/UTC time, 
then you might want to use OffsetDateTime.

## LocalDate
{% gist nitinkc/79309bfcaf2b3f44c993e827cecd5814 %}

## LocalDateTime
{% gist nitinkc/cae344eab0c8d789d2013665eefd9272 %}

## ZonedDateTime
**Parse Input String into ZonedDate time**
{% gist nitinkc/c82dd66846fe166d5ac5d7d40b9d87ff %}

**Format ZonedDateTime into desired output String format (to be used as json strings)**
{% gist nitinkc/4621ddf2c4efa980dfe32b89aa63bb1e %}

### ZoneId vs ZoneOffset

```java
//TimeZone
ZoneId zone    = ZoneId.systemDefault();//Uses Z for UTC
ZoneId india   = ZoneId.of("Asia/Kolkata");//UTC+05:30
ZoneId chicago = ZoneId.of("US/Central");
ZoneId ny      = ZoneId.of("UTC-05:00");
```
**ZoneId**
- Represents a time zone identifier, such as "America/New_York" or "Europe/London".
- It provides a way to identify regions with distinct rules for adjusting time, 
including daylight saving time (DST) rules.
- ZoneId is used to create ZonedDateTime instances, which represent a specific date and time in a particular time zone.

**ZoneOffset**
- Represents a fixed offset from UTC, such as +03:00 or -08:00.
- It **_does not handle_** daylight saving time or historical changes in time zone rules; 
it simply represents a constant time difference from UTC.
```java
String ist = ZoneOffset.SHORT_IDS.get("IST");//Asia/Kolkata
//Get zoneOffset from Zone Id
ZoneOffset standardOffset =  zoneId.getRules().getStandardOffset(Instant.now()).toString();//+05:30
```
# A case with Z
As per [Java 17 documentation](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/text/SimpleDateFormat.html)

Capital Z would format the date with timezone in the end with + or - sign indicating the timezone compared to UTC. 
{% gist nitinkc/22f8f3ea4afcf340d49a2610407297fc %}

For ZoneDateTime 
`yyyy-MM-dd'T'HH:mm:ss.SSSZ` format would look like `2022-03-03T09:08:56.064+0000`  


## Date comparison with ZonedDateTime 
It is easy to compare the dates with `ZonedDateTime`

{% gist nitinkc/7e3dc6cb2ac498e478a8a1d92b3537f9 %}

# Convertors

Working with Legacy DB that uses Timestamp

> toInstant connects ZonedDateTime with sql Timestamp

Java provides a way to convert between ZonedDateTime and Timestamp using the `toInstant()`

```java
//converts a ZonedDateTime to a Timestamp
Timestamp timestamp = Timestamp.from(ZonedDateTime.now(ZoneOffset.UTC).toInstant());

//converts a Timestamp to a ZonedDateTime
ZonedDateTime zonedDateTime = timestamp.toInstant().atZone(ZoneOffset.UTC);
```

# from SQL Timestamp

SQL Timestamp to LocalDate

SQL Timestamp to LocalDateTime

### SQL Timestamp to ZonedDateTime 

Often the timestamp conversion is needed to and from DB timestamp column

{% gist nitinkc/bdb6c5617386b920c5ca1d4aacc708b7 %}

## to SQL Timestamp

SQL Timestamp has Date and Time component. Thus, LocalDateTime is the connecting medium.

### LocalDate to SQL Timestamp
Instead of just using Date, convert the Date into DateTime by using `startOfDay` or `endOfDay` to properly 
convert into SQL Timestamp

### LocalDateTime to SQL Timestamp

{% gist nitinkc/11cc696554e57fb40327223f5f349de4 %}


### ZonedDateTime to SQL Timestamp

```java
public static Timestamp fromDate(ZonedDateTime date) {
    return Optional.of(Timestamp.valueOf(date.toLocalDateTime())).orElse(null);
}
```

{% gist nitinkc/1c5a4ee935450d075580e40108a8b413 %}


### SQL Timestamp from current time with UTC timezone 

Often, to save current time stamp in DB (ex. updateTime column in a table), with multiple timezones, it is a good idea to save in UTC 
```java
public static Timestamp currentTimestamp() {
        return Timestamp.from(ZonedDateTime.now(ZoneOffset.UTC).toInstant());
    }
```

# Letters Meaning

| Symbol | Examples                                       | Meaning                    |
|:------:|:-----------------------------------------------|:---------------------------|
|   G    | AD; Anno Domini; A                             | era                        |
|   u    | 2004; 04                                       | year                       |
|   y    | 2004; 04                                       | year-of-era                |
|   Y    | 1996; 96                                       | week-based-year            |
|   D    | 189                                            | day-of-year                |
|   d    | 10                                             | day-of-month               |
|  M/L   | 7; 07; Jul; July; J                            | month-of-year              |
|        |                                                |                            |
|  Q/q   | 3; 03; Q3; 3rd quarter                         | quarter-of-year            |
|   w    | 27                                             | week-of-week-based-year    |
|   W    | 4                                              | week-of-month              |
|   E    | Tue; Tuesday; T                                | day-of-week                |
|  e/c   | 2; 02; Tue; Tuesday; T                         | localized day-of-week      |
|   F    | 3                                              | week-of-month              |
|        |                                                |                            |
|   a    | PM                                             | am-pm-of-day               |
|   h    | 12                                             | clock-hour-of-am-pm (1-12) |
|   K    | 0                                              | hour-of-am-pm (0-11)       |
|   k    | 0                                              | clock-hour-of-am-pm (1-24) |
|        |                                                |                            |
|   H    | 0                                              | hour-of-day (0-23)         |
|   m    | 30                                             | minute-of-hour             |
|   s    | 55                                             | second-of-minute           |
|   S    | 978                                            | fraction-of-second         |
|   A    | 1234                                           | milli-of-day               |
|   n    | 987654321                                      | nano-of-second             |
|   N    | 1234000000                                     | nano-of-day                |
|        |                                                |                            |
|   v    | America/Los_Angeles                            | time-zone ID               |
|   Z    | -08:30                                         |                            |
|   z    | Pacific Standard Time; PST                     | time-zone name             |
|   O    | GMT+8; GMT+08:00; UTC-08:00;                   | localized zone-offset      |
|   X    | Z; -08; -0830; -08:30; -083015; -08:30:15;     | zone-offset 'Z' for zero   |
|   x    | +0000; -08; -0830; -08:30; -083015; -08:30:15; | zone-offset                |
|   Z    | +0000; -0800; -08:00;                          | zone-offset                |