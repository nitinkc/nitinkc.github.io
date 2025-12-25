---
categories: Developer Tools
date: 2023-11-10 21:55:00
tags:
- IntelliJ
- IDE
- Debugging
- Tips
- Shortcuts
title: IntelliJ Idea Debug
---

{% include toc title="Index" %}

## Debug : Get object as JSON

See the Java Object using jackson mapper conversion

```java
new com.fasterxml.jackson.databind.ObjectMapper()
    .registerModule(new com.fasterxml.jackson.datatype.jsr310.JavaTimeModule())
    .disable(com.fasterxml.jackson.databind.SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
    .setSerializationInclusion(com.fasterxml.jackson.annotation.JsonInclude.Include.ALWAYS)
    .writerWithDefaultPrettyPrinter()
    .writeValueAsString( obj );
```

# Show ByteCode

![showByteCode.png](/assets/images/intelliJ/showByteCode.png)