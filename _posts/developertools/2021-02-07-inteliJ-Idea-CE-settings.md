---
# layout: static
title:  "IntelliJ Idea settings"
date:   2021-02-07 02:15:00
categories: ['Developer tools']
tags: ['Developer tools']
sidebar:
  nav: "algo"
---

## Contents

{% include toc title="Index" %}

# Initial Settings

For the personalized comments, use the following the templates in the Preferences as below

Goto : `Preferences -> Editor -> File and Code Templates`

and use the following pattern

```
/**
* Created by ${USER} on ${DAY_NAME_FULL}, ${MONTH_NAME_FULL}/${DAY}/${YEAR} at ${TIME}
*/
```

![](/assets/images/intelliJ/intelliJ.png)



![](/assets/images/intelliJ/2lineTabs.png)


## Open the working Tabs on the left side.

##### Ensure to check the MARK MODIFIED check box.

![](/assets/images/intelliJ/tabsLeft.png)

##### In one Row
If opening on the top, uncheck the "Show tabs in one row, so that all the 
tabs appear like this
![](/assets/images/intelliJ/oneRowTab.png)

## Hide Usages
![](/assets/images/intelliJ/hideUsages.png)

## Change Font size
![changeFont.png]((/assets/images/intelliJ/changeFont.png))


## Hard Wrap
![]((/assets/images/intelliJ/hardWrap.png))

# Useful Plugins

Scenario : When entity or DTO classes have lots of fields, it is easy to miss fileds that are set,
to Generate all Setters for long entity classes, use this plugin

[Generate All Setters](https://plugins.jetbrains.com/plugin/9360-generateallsetter)

Scenario : Converting application.properties into aplication.yml

[properties to yml convert](https://plugins.jetbrains.com/plugin/8000-properties-to-yaml-converter)

Scenario: While converting maven project to Gradle. USe this plugin for converting pom dependencies into gradle.

[Pom to Gradle](https://plugins.jetbrains.com/plugin/7937-gradle-dependencies-formatter)

# New UI

Classic screen most used features

**Top Left**

* Back CMD [
* FWD CMD ]

**Sidebar**

**Left**
* Project
* Commit
* Structure
* Bookmark

**Right**
* Gradle
* Code Coverage

![classic_intelliJ.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2Fclassic_intelliJ.png)

##### Customize the Toolbar on the new UI to match the exact items
![customize_toolbar_new_intelliJ.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2Fcustomize_toolbar_new_intelliJ.png)


![new_intelliJ.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2Fnew_intelliJ.png)