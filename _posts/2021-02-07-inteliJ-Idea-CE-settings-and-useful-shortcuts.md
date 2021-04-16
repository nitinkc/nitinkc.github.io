---
# layout: static
title:  "IntelliJ Idea - Useful settings and shortcuts"
date:   2021-02-07 02:15:00
categories: ['Developer tools']
tags: ['Developer tools']
sidebar:
  nav: "algo"
---

## Contents

{% include toc title="Index" %}

# Useful Shortcuts
| S.no| Shortcut                 | Use                              |
|---- |--------------------------|----------------------------------|
| 1  | cntl + shift + N | Find class/interface files  |
| 2  | |

# Initial Settings 

For the personalized comments, use the following the templates in the Preferences as below

Goto : `Preferences -> Editor -> File and Code Templates`

and use the following pattern

```
/**
* Created by ${USER} on ${DAY_NAME_FULL}, ${MONTH_NAME_FULL}/${DAY}/${YEAR} at ${TIME}
*/
```

![](/assets/images/intelliJ.png)

## Useful Plugins

Scenario : When entity or DTO classes have lots of fields, it is easy to miss fileds that are set,
to Generate all Setters for long entity classes, use this plugin

[Generate All Setters](https://plugins.jetbrains.com/plugin/9360-generateallsetter)

Scenario : Converting application.properties into aplication.yml

[properties to yml convert](https://plugins.jetbrains.com/plugin/8000-properties-to-yaml-converter)

Scenario: While converting maven project to Gradle. USe this plugin for converting pom dependencies into gradle.

[Pom to Gradle](https://plugins.jetbrains.com/plugin/7937-gradle-dependencies-formatter)

