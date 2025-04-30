---
title: "Deployment process - From Dev to Release"
date: 2025-04-29 05:00:00
categories: [ DevOps ]
tags: [ DevOpsDevOps ]
---
{% include toc title="Index" %}

The full cycle from code changes to deployment for a Spring Boot Java application on Google Kubernetes Engine (GKE) is as below

### **1. Code Changes**
- **Development**: Developers write code using Spring Boot for Java applications.
- **Version Control**: Code is committed to a version control system like Git.

### **2. Continuous Integration (CI)**
- **Build**: Jenkins or another CI tool automatically builds the application whenever code changes are pushed to the repository.
- **Test**: Automated tests are run to ensure the code changes don't break existing functionality.
- **Static Code Analysis**: Tools like SonarQube are used for static code analysis to ensure code quality.
  ```xml
  <!-- Add SonarQube plugin to build.gradle -->
  plugins {
      id "org.sonarqube" version "3.4.0.905"
  }
  ```

#### **2.1. Containerization**
- **Docker**: The application is containerized using Docker, creating a Docker image via Jenkins Pipeline
  ```dockerfile
  FROM openjdk:11-jre-slim
  COPY build/libs/myapp.jar /app.jar
  ENTRYPOINT ["java", "-jar", "/app.jar"]
  ```

### **4. Continuous Delivery (CD)**
- **Helm Charts**: Helm charts are used to **define the Kubernetes resources** needed to deploy the application.
- **Terraform**: Terraform provisions the necessary infrastructure, such as Kubernetes clusters on GKE.
  ```hcl
  provider "google" {
    project = "my-gcp-project"
    region  = "us-central1"
  }

  resource "google_container_cluster" "primary" {
    name     = "my-gke-cluster"
    location = "us-central1"
  }
  ```

### **5. Deployment**
- **Helm**: Helm deploys the application to the Kubernetes cluster.
  ```yaml
  # Helm chart values.yaml
  image:
    repository: myapp
    tag: latest
  service:
    type: LoadBalancer
    port: 80
  ```
- **Flux**: Flux monitors the Git repository for changes and automatically updates the Kubernetes cluster with the latest Helm charts.
  ```yaml
  apiVersion: fluxcd.io/v1
  kind: HelmRelease
  metadata:
    name: myapp
  spec:
    releaseName: myapp
    chart:
      repository: https://charts.myrepo.com
      name: myapp
      version: 1.0.0
  ```

### **6. Monitoring and Maintenance**
- **Monitoring**: Tools like Prometheus and Grafana are used to monitor the application's performance and health.
  ```yaml
  # Prometheus configuration in application.yaml
  management:
    endpoints:
      web:
        exposure:
          include: health,info,prometheus
  ```
- **Dynatrace**: Dynatrace can be used to monitor application performance.
  ```xml
  <!-- Add Dynatrace Micrometer registry to build.gradle -->
  dependencies {
      implementation "com.dynatrace.microservices:dynatrace-micrometer-registry:1.7.0"
  }
  ```
- **Updates**: Continuous updates and improvements are made based on feedback and monitoring data.

### **Connecting the Dots**
1. **Code Changes**: Developers push code to Git.
2. **CI/CD**: Jenkins builds, tests, and deploys the application.
3. **Containerization**: Docker creates a container image.
4. **Provisioning**: Terraform sets up the GKE cluster.
5. **Deployment**: Helm deploys the application to GKE.
6. **GitOps**: Flux automates deployments based on Git changes.
7. **Monitoring**: Dynatrace and Prometheus monitor the application's performance and health.
