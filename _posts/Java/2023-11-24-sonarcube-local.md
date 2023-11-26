---
title:  "Sonarcube on local"
date:   2023-11-24 12:17:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

# Run sonarcube from Docker
```shell
docker run -d \
  --name sonarqube \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  -p 9000:9000 \
  sonarqube:latest
```

## Run sonarcube analysis

**Local project**
- Open sonarcube and create a new Local project
[http://localhost:9000/projects](http://localhost:9000/projects)
- provide project display name, project key, main branch name

**Set up project for Clean as You Code**
- Use the global Setting

**Analysis Method** 
- locally

**Analyze your project**
1. Provide a token
2. Run analysis on your project

##### Gradle Project

```shell
./gradlew sonar \
  -Dsonar.projectKey=JavaConcepts \
  -Dsonar.projectName='JavaConcepts' \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqp_4bc2edb73227baac04fe2fa8ba546263f2d2e12a
```

##### Maven Project

```shell
mvn clean verify sonar:sonar \
-Dsonar.projectKey=Mockito \
-Dsonar.projectName='Mockito' \
-Dsonar.host.url=http://localhost:9000 \
-Dsonar.token=sqp_6e746c1c1ff4b34c535c341ff38299463d9ea005
```
