---
# layout: static
title:  "IntelliJ Idea settings"
date:   2021-02-07 02:15:00
categories: ['Developer tools']
tags: ['Developer tools']
sidebar:
  nav: "algo"
---

{% include toc title="Index" %}

# Comments on new Class File created

For the personalized comments, use the following the template in the Preferences as below

Goto : `Preferences -> Editor -> File and Code Templates` and create a pattern of choice

```java
/**
* Created by ${USER} on ${DAY_NAME_FULL}, ${MONTH_NAME_FULL}/${DAY}/${YEAR} at ${TIME}
*/
```

![](/assets/images/intelliJ/intelliJ.png)

# Show line numbers and Method separator
![show_lineNumbers.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2Fshow_lineNumbers.png)

# Configure Tabs
![](/assets/images/intelliJ/2lineTabs.png)

Ensure to check the MARK MODIFIED check box and Open the working Tabs on the left side.
![](/assets/images/intelliJ/tabsLeft.png)

##### Arrange Tab in two rows on Top
If opening on the top, uncheck the "Show tabs in one row, so that all the tabs appear like this
![](/assets/images/intelliJ/oneRowTab.png)

##### Show Pinned Tab in Separate Row
![pinned_tab.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2Fpinned_tab.png)

# Configure font size for Presenting
![font_size.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2Ffont_size.png)

##### Change Editor Font
![changeFont.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2FchangeFont.png)

# Hide Usages
![](/assets/images/intelliJ/hideUsages.png)

# Hard Wrap
![hardWrap.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2FhardWrap.png)

# Useful Plugins

[Generate All Setters](https://plugins.jetbrains.com/plugin/9360-generateallsetter)
* When entity or DTO classes have lots of fields, it is easy to miss fields that are set,
to Generate all Setters for long entity classes, use this plugin

[properties to yml convert](https://plugins.jetbrains.com/plugin/8000-properties-to-yaml-converter)
* Converting application.properties into aplication.yml

[Pom to Gradle](https://plugins.jetbrains.com/plugin/7937-gradle-dependencies-formatter)
* While converting maven project to Gradle. USe this plugin for converting pom dependencies into gradle.

##### List of all downloaded plugins, 

Select all (CTRL+A) and copy for a list of installed Plugins
![downloaded_plugin.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2Fdownloaded_plugin.png)


```log
.env files support (2023.2)
CodeGlance Pro (1.7.6)
Docker (232.10203.2)
EnvFile (3.4.1)
google-java-format (1.17.0.0)
Gradianto (5.5)
Lightrun (1.19.0-release.3b9e786f14)
Lombok (232.10203.10)
One Dark theme (5.9.0)
Package Search (232.9921.28)
Pieces | Save, Search, Share & Reuse Code Snippets (6.3.0)
Presentation Assistant (1.0.10)
Rainbow Brackets (2023.3.7)
Randomness (2.7.7)
RoboPOJOGenerator (2.4.1)
Snyk Security - Code, Open Source, Container, IaC Configurations (2.5.6)
Solarized Theme (3.0.0)
SonarLint (10.0.1.77000)
wl Spring Assistant (1.4.6.222.232)
```

# New UI

Classic screen most used features

**Top Left** : Back button `CMD [` , Forward `CMD ]`

**Sidebar**
* **Left** : Project, Commit, Structure, Bookmark
* **Right** : Gradle, Code Coverage

![classic_intelliJ.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2Fclassic_intelliJ.png)

##### Customize the Toolbar
![customize_toolbar_new_intelliJ.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2Fcustomize_toolbar_new_intelliJ.png)

# Final look 
![new_intelliJ.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2Fnew_intelliJ.png)


# Show ByteCode
![showByteCode.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2FshowByteCode.png)

# Flatten the package
![flattenPackages.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2FflattenPackages.png)

# Enable Auto restart with Devtools

Put the dependency in the gradle/maven file

```shell
// https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-devtools
implementation group: 'org.springframework.boot', name: 'spring-boot-devtools', version: '3.2.3'
```
Make the following changes in the intelliJ settings
![autoRestart1.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2FautoRestart1.png)

![autoRestart2.png](..%2F..%2Fassets%2Fimages%2FintelliJ%2FautoRestart2.png)