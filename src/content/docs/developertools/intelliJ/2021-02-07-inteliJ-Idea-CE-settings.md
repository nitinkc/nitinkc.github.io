---
title: IntelliJ Idea settings
date: 2021-02-07 02:15:00
categories:
- Developer Tools
tags:
- IntelliJ
- IDE
- Settings
- Configuration
- Setup
sidebar:
  nav: algo
---

{% include toc title="Index" %}

# Comments on new Class File created

For the personalized comments, use the following the template in the Preferences
as below

Goto : `Preferences -> Editor -> File and Code Templates` and create a pattern
of choice

```java
/**
* Created by ${USER} on ${DAY_NAME_FULL}, ${MONTH_NAME_FULL}/${DAY}/${YEAR} at ${TIME}
*/
```

![](/assets/images/intelliJ/intelliJ.png)

# Show line numbers and Method separator

![show_lineNumbers.png](/assets/images/intelliJ/show_lineNumbers.png)

# Configure Tabs

![](/assets/images/intelliJ/2lineTabs.png)

Ensure to check the MARK MODIFIED check box and Open the working Tabs on the
left side.
![](/assets/images/intelliJ/tabsLeft.png)

##### Arrange Tab in two rows on Top

If opening on the top, uncheck the "Show tabs in one row, so that all the tabs
appear like this
![](/assets/images/intelliJ/oneRowTab.png)

##### Show Pinned Tab in Separate Row

![pinned_tab.png](/assets/images/intelliJ/pinned_tab.png)

# Configure font size for Presenting

![font_size.png](/assets/images/intelliJ/font_size.png)

##### Change Editor Font

![changeFont.png](/assets/images/intelliJ/changeFont.png)

# Hide Usages

![](/assets/images/intelliJ/hideUsages.png)

# Hard Wrap

![hardWrap.png](/assets/images/intelliJ/hardWrap.png)

# Useful Plugins

[Generate All Setters](https://plugins.jetbrains.com/plugin/9360-generateallsetter)

* When entity or DTO classes have lots of fields, it is easy to miss fields that
  are set,
  to Generate all Setters for long entity classes, use this plugin

[properties to yml convert](https://plugins.jetbrains.com/plugin/8000-properties-to-yaml-converter)

* Converting application.properties into aplication.yml

[Pom to Gradle](https://plugins.jetbrains.com/plugin/7937-gradle-dependencies-formatter)

* While converting maven project to Gradle. USe this plugin for converting pom
  dependencies into gradle.

##### List of all downloaded plugins,

Select all (CTRL+A) and copy for a list of installed Plugins
![downloaded_plugin.png](/assets/images/intelliJ/downloaded_plugin.png)

- .env files support (2023.2)
- CodeGlance Pro (1.7.6)
- Docker (232.10203.2)
- EnvFile (3.4.1)
- google-java-format (1.17.0.0)
- Gradianto (5.5)
- Lightrun (1.19.0-release.3b9e786f14)
- Lombok (232.10203.10)
- One Dark theme (5.9.0)
- Package Search (232.9921.28)
- Pieces | Save, Search, Share & Reuse Code Snippets (6.3.0)
- Presentation Assistant (1.0.10)
- Rainbow Brackets (2023.3.7)
- Randomness (2.7.7)
- RoboPOJOGenerator (2.4.1)
- Snyk Security - Code, Open Source, Container, IaC Configurations (2.5.6)
- Solarized Theme (3.0.0)
- SonarLint (10.0.1.77000)
- wl Spring Assistant (1.4.6.222.232)

# New UI

Classic screen most used features

**Top Left** : Back button `CMD [` , Forward `CMD ]`

**Sidebar**

* **Left** : Project, Commit, Structure, Bookmark
* **Right** : Gradle, Code Coverage

![classic_intelliJ.png](/assets/images/intelliJ/classic_intelliJ.png)

##### Customize the Toolbar

![customize_toolbar_new_intelliJ.png](/assets/images/intelliJ/customize_toolbar_new_intelliJ.png)

# Final look

![new_intelliJ.png](/assets/images/intelliJ/new_intelliJ.png)

# Show ByteCode

![showByteCode.png](/assets/images/intelliJ/showByteCode.png)

# Flatten the package

![flattenPackages.png](/assets/images/intelliJ/flattenPackages.png)

# Enable Auto restart with Devtools

Put the dependency in the gradle/maven file

```shell
// https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-devtools
implementation group: 'org.springframework.boot', name: 'spring-boot-devtools', version: '3.2.3'
```

Make the following changes in the intelliJ settings
![autoRestart1.png](/assets/images/intelliJ/autoRestart1.png)

![autoRestart2.png](/assets/images/intelliJ/autoRestart2.png)

# Enable SonarCube

Install the SonarLint plugin and configure it in IntelliJ

![sonar1.png](/assets/images/intelliJ/sonar1.png)

Add & Configure the Connection
![sonar2.png](/assets/images/intelliJ/sonar2.png)
Set the Token, instead of user/password
![sonar3.png](/assets/images/intelliJ/sonar3.png)

# Enable Google Code Format

![google-format1.png](/assets/images/intelliJ/google-format1.png)

![google-format2.png](/assets/images/intelliJ/google-format2.png)

# Enable Font Zoom/Font Size change

![font-zoom.png](/assets/images/intelliJ/font-zoom.png)


# Invalidate Caches and Restore

![invalidateCache.png]({{ site.url }}/assets/images/intelliJ/invalidateCache.png){:width="70%" height="50%"}