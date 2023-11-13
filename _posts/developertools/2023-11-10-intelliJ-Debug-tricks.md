---
# layout: static
title:  "IntelliJ Idea Debug"
date:   2021-11-03 21:55:00
categories: Shortcuts
tags: [Shortcuts]
---

{% include toc title="Index" %}

## Debug : Get object as JSON 
```java
new ObjectMapper()
  .setSerializationInclusion(JsonInclude.Include.NON_NULL)
  .writerWithDefaultPrettyPrinter()
  .writeValueAsString( obj )
```

See the Java Object using jackson mapper conversion

```java
new com.fasterxml.jackson.databind.ObjectMapper()
.registerModule(new com.fasterxml.jackson.datatype.jsr310.JavaTimeModule())
.disable(com.fasterxml.jackson.databind.SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
.writerWithDefaultPrettyPrinter()
.writeValueAsString( obj );
```
