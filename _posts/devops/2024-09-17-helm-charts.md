---
categories: DevOps
date: 2024-09-17 23:02:00
tags:
- Kubernetes
- Charts
- Package Manager
title: Helm Charts with minikube
---

{% include toc title="Index" %}

```shell
helm repo list
helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo remove bitnami
```

# Search the repository:

```shell
helm search repo mysql

helm search repo database

helm search repo database --versions
```

# Installation

## Default namespace

```shell
helm install mydb bitnami/mysql
```

## custom namespace

```shell
# Create a namespace
kubectl create ns non-prod

helm install --namespace non-prod mydb bitnami/mysql
helm install --n non-prod mydb2 bitnami/mysql
```

# Check the cluster and docker

```shell
kubectl get pods

minikube ssh

docker images
```

# To check the installation status:

```shell
helm status mydb
```

# Upgrade:

Get the default password

`ROOT_PASSWORD=$(kubectl get secret --namespace default mydb-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode)`

```shell
helm upgrade --namespace default mysql-release bitnami/mysql --set auth.rootPassword=$ROOT_PASSWORD
```

# Uninstallation

```shell
helm uninstall mysql-release
```

## Create custom helm charts

```shell
helm create my-first-chart
helm package my-first-chart
helm repo index .
```

Update the repo

```shell
helm repo update
```

Install

```shell
helm repo add myrepo https://nitinkc.github.io/HelmCharts
```

```shell
helm install myapp myrepo/my-first-chart
```

Changes in
the [values file](https://github.com/nitinkc/HelmCharts/blob/main/todo-app/values.yaml#L10-L58)

# Docker image

```shell
helm create todo-app
```

- Remove hpa, ingress, serviceaccount yamls
- remove anything related to serviceaccount from helper and deployment yml

Docker hub
[https://hub.docker.com/repository/docker/nitinkc/todo-app/tags](https://hub.docker.com/repository/docker/nitinkc/todo-app/tags)

Changes pertaining to Dockerimage
[https://github.com/nitinkc/HelmCharts/commit/bb599c519d66dcb7de5a4457b9e36d33f64cdf0e](https://github.com/nitinkc/HelmCharts/commit/bb599c519d66dcb7de5a4457b9e36d33f64cdf0e)

After helm file changes

```shell
helm package todo-app
helm repo index . 

# Git push
helm repo update 
```

Install

```shell
helm install todo-service-app myrepo/todo-app 
```

Upgrade

```shell
helm upgrade --install todo-service-app myrepo/todo-app
```

to avoid the hassles of commit and repo update, try

```shell
cd todo-app
helm upgrade --install todo-service-app myrepo/todo-app -f values.yaml
```

# Interact with the pod

Get the IP's, names etc from `minikube dashboard`

Check logs

```shell
#pod name from minikube Dashboard
kubectl logs todo-service-app-todo-app-7b45c8749b-ltmfw  
kubectl logs -f todo-service-app-todo-app-7b45c8749b-ltmfw    
```

Test Connectivity from Inside the Pod

use a temporary pod to check if the application is reachable from within the
cluster

```shell
kubectl run -it --rm --restart=Never busybox --image=busybox -- sh
```

Then, inside the busybox shell, try to curl your application:

```shell
wget -qO- http://<your-pod-ip>:5000/actuator/health
```


```sh
docker run -d --name oci-registry -p 5000:5000 registry

helm package firstchart

helm push firstchart-0.1.0.tgz oci://localhost:5000/helm-charts

helm show all oci://localhost:5000/helm-charts/firstchart --version 0.1.0

helm pull oci://localhost:5000/helm-charts/firstchart --version 0.1.0

helm template myrelease oci://localhost:5000/helm-charts/firstchart --version 0.1.0

helm install myrelease oci://localhost:5000/helm-charts/firstchart --version 0.1.0

helm upgrade myrelease oci://localhost:5000/helm-charts/firstchart --version 0.2.0

helm registry login -u myuser <oci registry>

helm registry logout <oci registry url>
```