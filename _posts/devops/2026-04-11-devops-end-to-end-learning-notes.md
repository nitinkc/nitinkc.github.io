---
title: "DevOps End-to-End — Learning Notes for Developers"
date: 2026-04-11 00:30:00
categories:
- DevOps
tags:
- CI/CD
- Pipeline
- Kubernetes
- Infrastructure
- Automation
- Monitoring
toc: true
toc_label: "Index"
---

{% include toc title="Index" %}

# The Big Picture — Full Pipeline at a Glance

Every modern cloud deployment follows roughly the same end-to-end journey:

```
Developer → Git Commit
    → CI Server (Jenkins)
        → Build (Gradle/Maven)
        → Unit Tests
        → Static Analysis (SonarQube)
        → Docker Build + Push to Registry
    → CD Pipeline
        → Terraform (provision GKE infra — runs once / when infra changes)
        → Helm (deploy/upgrade application — runs every release)
        → GitOps (Flux watches Git, auto-syncs cluster)
    → Running Application on GKE
        → Monitoring (Prometheus + Grafana, Datadog, Dynatrace)
```

**Key mental model:**
- **Terraform** = _infrastructure_ layer (create the Kubernetes cluster itself)
- **Helm** = _application_ layer (deploy your app _onto_ the cluster)
- **Flux** = _automation_ layer (keep the cluster in sync with what's in Git)

These three tools answer three different questions:

| Question                              | Tool                                 |
|:--------------------------------------|:-------------------------------------|
| Where does the app run?               | Terraform                            |
| How is the app packaged and deployed? | Helm                                 |
| Who triggers the deployment?          | Jenkins (push) or Flux (pull/GitOps) |


# Step 1 — Code Changes and Version Control

- Developers write **Spring Boot** application code.
- Code is committed to a **Git** repository (GitHub, GitLab, Bitbucket, etc.).
  - A pull request / merge triggers the CI pipeline automatically via [**webhooks**]({% post_url systems_design/networks/2024-06-28-WebHooks %}).

**Branching strategy tip**: Most teams use `develop` for QA and `relese` for production and
Merging to `develop/release` triggers a build pipeline.


# Step 2 — Continuous Integration (CI)

CI means: _every commit is automatically built, tested, and validated_.

## 2.1 Jenkins Pipeline

Jenkins is the most common CI server in enterprise Java shops. Pipelines are defined as code in a `Jenkinsfile`:

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh './gradlew clean build -x test'
            }
        }
        stage('Unit Tests') {
            steps {
                sh './gradlew test'
            }
            post {
                always {
                    junit 'build/test-results/**/*.xml'
                }
            }
        }
        stage('Static Analysis (SonarQube)') {
            steps {
                sh './gradlew sonarqube'
            }
        }
        stage('Docker Build & Push') {
            steps {
                script {
                    def image = docker.build("gcr.io/my-project/myapp:${env.BUILD_NUMBER}")
                    docker.withRegistry('https://gcr.io', 'gcr-credentials') {
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
    }
}
```

## 2.2 Static Code Analysis — SonarQube

SonarQube scans code for:
- **Bugs** — potential runtime errors
- **Vulnerabilities** — security issues (e.g., SQL injection risk)
- **Code Smells** — maintainability issues
- **Coverage** — what % of code is covered by tests

Add to `build.gradle`:

```groovy
plugins {
    id "org.sonarqube" version "3.4.0.905"
}
```

A **quality gate** is a pass/fail threshold (e.g., "coverage must be ≥ 80%").
Jenkins can be configured to fail the build if the gate is not met.

## 2.3 Containerization — Docker

Docker packages the application + its runtime into a portable, reproducible **image**. 
The image is the artifact that gets deployed everywhere.

```dockerfile
# Build stage
FROM gradle:7.6-jdk17 AS builder
WORKDIR /app
COPY . .
RUN gradle build -x test

# Runtime stage (smaller final image)
FROM openjdk:17-jre-slim
COPY --from=builder /app/build/libs/myapp.jar /app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

The built image is **pushed to a container registry**:
- **Google Container Registry (GCR)**: `gcr.io/my-project/myapp:1.2.3`
- **Docker Hub**: `myorg/myapp:1.2.3`
- **Artifact Registry** (modern GCP): `us-central1-docker.pkg.dev/my-project/my-repo/myapp:1.2.3`

Once pushed, the image tag (e.g., `:1.2.3` or `:${BUILD_NUMBER}`) is used by Helm to tell Kubernetes _exactly_ which image to run.

# Step 3 — Infrastructure Provisioning with Terraform

**Terraform** answers: _"Where does the application run?"_

It provisions the **cloud infrastructure** — before you can deploy an app to
Kubernetes, you need a Kubernetes cluster. That cluster **is created** by Terraform.

## 3.1 What Terraform manages

- Google Kubernetes Engine (GKE) clusters (the Kubernetes cluster itself)
- VPCs, subnets, firewall rules
- IAM roles and service accounts
- Cloud SQL databases, Cloud Storage buckets
- Load balancers and DNS entries

**Key principle**: Terraform uses **HCL (HashiCorp Configuration Language)** to
describe _**desired state**_. It figures out what needs to be created/changed/deleted.

## 3.2 Terraform Lifecycle Commands

```bash
terraform init      # Download providers & modules (run once per workspace)
terraform plan      # Preview changes — shows what WILL be created/modified/destroyed
terraform apply     # Apply changes to real infrastructure
terraform destroy   # Tear down all managed resources
```

Always run `terraform plan` before `apply` in production — it's your safety net.

## 3.3 GKE Cluster Example

```hcl
provider "google" {
  credentials = file("<path-to-service-account>.json")
  project     = "<your-project-id>"
  region      = "us-central1"
}

resource "google_container_cluster" "primary" {
  name     = "my-gke-cluster"
  location = "us-central1-a"

  initial_node_count = 3

  node_config {
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}
```

## 3.4 Terraform vs Helm — When does each run?

|                     | Terraform                                    | Helm                                               |
|:--------------------|:---------------------------------------------|:---------------------------------------------------|
| **What it manages** | Cloud infrastructure (cluster, network, IAM) | Application workloads running _inside_ the cluster |
| **How often**       | Once at setup; re-run when infra changes     | Every app release / config change                  |
| **Triggered by**    | Infra team PR merged to infra repo           | App CI/CD pipeline                                 |
| **State stored in** | Remote state (GCS bucket, Terraform Cloud)   | Kubernetes secrets (in-cluster)                    |


# Step 4 — Application Deployment with Helm

**Helm** answers: _"How is the application packaged and deployed onto Kubernetes?"_

Think of Helm as `apt` or `brew` for Kubernetes — it packages all the YAML
manifests your app needs into a single versioned **chart**, and lets you install,
upgrade, and roll back with simple commands.

## 4.1 What a Helm Chart looks like

```
charts/
└── my-application/
    ├── Chart.yaml          ← metadata (name, version, description)
    ├── values.yaml         ← default configuration values
    ├── requirements.yaml   ← chart dependencies (e.g., Postgres chart)
    └── templates/
        ├── deployment.yaml ← Kubernetes Deployment manifest
        ├── service.yaml    ← Kubernetes Service manifest
        ├── ingress.yaml    ← Ingress / load balancer config
        └── config.yaml     ← ConfigMaps / Secrets
```

## 4.2 values.yaml — The configuration knob

Environment-specific values (dev vs staging vs prod) are set here or overridden
at deploy time:

```yaml
# values.yaml
replicaCount: 2

image:
  repository: gcr.io/my-project/myapp
  tag: "latest"          # Overridden in CI to a specific build tag
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80
  targetPort: 8080

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

env:
  DATABASE_URL: "jdbc:postgresql://my-db:5432/myapp"
```

## 4.3 Deploy / Upgrade command (used in Jenkinsfile)

```groovy
stage('Deploy to Kubernetes') {
    steps {
        script {
            sh '''
              helm upgrade --install my-application ./charts/my-application \
                --values ./charts/my-application/values.yaml \
                --set image.tag=${BUILD_NUMBER} \
                --namespace production \
                --wait
            '''
        }
    }
}
```

- `--install` means: install if not already deployed, otherwise upgrade.
- `--set image.tag=${BUILD_NUMBER}` injects the exact Docker image tag from CI.
- `--wait` blocks until all pods are running (fail fast if something is wrong).

## 4.4 Rollback

```bash
# See release history
helm history my-application -n production

# Roll back to the previous release
helm rollback my-application -n production

# Roll back to a specific revision
helm rollback my-application 3 -n production
```

This is why Helm is powerful — rolling back an entire application (all K8s
resources) is a single command.

---

# Step 5 — GitOps with Flux

**Flux** answers: _"Who keeps the cluster in sync with what's in Git?"_

## 5.1 GitOps Principle

> Git is the **single source of truth** for what should be running in the cluster.

Instead of running `helm upgrade` manually or from Jenkins (a **push** model),
Flux runs _inside_ the cluster and continuously watches the Git repo. When it
detects a change (new Helm chart version, updated values), it automatically
applies the change — a **pull** model.

```
Developer merges PR to config repo
         ↓
  Flux detects the change (polling Git every N minutes)
         ↓
  Flux runs `helm upgrade` internally
         ↓
  Kubernetes cluster updated
```

## 5.2 HelmRelease CRD

Flux uses custom Kubernetes resources. A `HelmRelease` tells Flux _which chart
to track and how to deploy it_:

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: myapp
  namespace: production
spec:
  interval: 5m                # How often Flux checks for changes
  releaseName: myapp
  chart:
    spec:
      chart: myapp
      version: "1.0.0"
      sourceRef:
        kind: HelmRepository
        name: my-charts-repo
  values:
    replicaCount: 3
    image:
      tag: "42"
```

## 5.3 Jenkins (Push) vs Flux (Pull) — When to use which

| | Jenkins Push | Flux Pull (GitOps) |
|---|---|---|
| **Deployment trigger** | Jenkins pipeline runs `helm upgrade` | Flux detects Git change, applies it |
| **Auditability** | Pipeline logs | Git commit history is the audit trail |
| **Drift detection** | No — cluster can diverge from Git | Yes — Flux continuously reconciles |
| **Best for** | Simple setups, fast feedback loops | Production-grade, compliance-heavy environments |

---

# Step 6 — Monitoring & Observability

Once deployed, you need to know if the application is healthy.

## 6.1 Three Pillars of Observability & Tools

| Pillar         | What it measures                           | Example Tools                                                                                                            | Best for Spring Boot                        |
|:---------------|:-------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------|
| **Metrics**    | CPU, memory, request rate, latency, errors | Prometheus (time-series DB) + Grafana (visualization) (free) / CloudWatch (AWS) / Azure Monitor / Cloud Monitoring (GCP) | Spring Boot Actuator `/actuator/prometheus` |
| **Logs**       | Application and system events              | ELK Stack (free) / CloudWatch Logs (AWS) / Log Analytics (Azure) / Cloud Logging (GCP)                                   | Spring Boot Logback + SLF4J                 |
| **Traces**     | Request path through microservices         | Jaeger (free) / Zipkin (free) / Datadog / Dynatrace                                                                      | Spring Cloud Sleuth or OpenTelemetry        |
| **All-in-one** | Metrics + Logs + Traces together           | Datadog / Dynatrace / New Relic / Splunk (paid)                                                                          | Automatic instrumentation via agents        |


# Step 7 — Connecting the Dots

Here is the full flow summarized in order:

1. **Code push**: Developer pushes code to Git (feature branch → PR → merge to `main`).
2. **CI triggers**: Jenkins detects the merge via webhook.
3. **Build & test**: Gradle builds the app, runs unit tests.
4. **Quality gate**: SonarQube analyzes code; build fails if gate not met.
5. **Docker image**: Jenkins builds and pushes a versioned Docker image to GCR.
6. **Infra (one-time)**: Terraform has already provisioned the GKE cluster, networking, and IAM.
7. **Deploy**: Jenkins runs `helm upgrade --install` with the new image tag — OR — a config repo PR updates the `HelmRelease` and Flux detects the change and deploys.
8. **Reconciliation**: Flux continuously ensures the cluster matches Git (drift detection).
9. **Monitoring**: Prometheus scrapes metrics; Grafana dashboards alert on anomalies; Dynatrace provides deep APM.


# Quick Reference — Common Interview Q&A

**Q: What is the difference between CI and CD?**
- **CI** (Continuous Integration): automatically build and test every commit.
- **CD** (Continuous Delivery/Deployment): automatically deliver tested artifacts to production (or a pre-prod environment).

**Q: What is the difference between Terraform and Helm?**
- Terraform provisions the **infrastructure** (the Kubernetes cluster, network, IAM on GCP).
- Helm deploys and manages **applications** inside an already-running Kubernetes cluster.

**Q: What is GitOps?**
- A practice where the entire desired state of the system (infrastructure + application config) is stored in Git. Automated agents (like Flux) continuously reconcile the cluster to match what is in Git.

**Q: What is the difference between a Jenkins push deployment and Flux?**
- Jenkins **pushes** a change to the cluster by running `helm upgrade` in a pipeline stage.
- Flux **pulls** — it watches Git and self-applies changes. Flux also detects and corrects **drift** (manual changes to the cluster that diverge from Git).

**Q: What does `helm upgrade --install` do?**
- If the release does not exist yet: installs it. If it already exists: upgrades it to the new chart/values. One command covers both cases.

**Q: How do you roll back a bad deployment?**
- `helm rollback <release-name> -n <namespace>` — reverts to the previous Helm revision in seconds.

**Q: What is a quality gate in SonarQube?**
- A set of conditions (e.g., code coverage ≥ 80%, no new critical bugs) that the codebase must meet. If the gate fails, CI marks the build as failed and the artifact is not promoted.
