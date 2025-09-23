---
categories: Microservices
date: 2022-10-11 20:35:00
tags:
- Spring Boot
title: Gradle - build & tool
---

# Gradle build tree

Use the reporting plugin to enable local build tree report

```groovy
plugins {
    id 'project-report'
}
// Or
apply plugin: 'project-report'
```

## Dependencies on command prompt

```sh
 gradle dependencies   
```

## Build Scan

```sh
gradle build --scan 
```

## Generate the html report

```sh
./gradlew htmlDependencyReport 
```