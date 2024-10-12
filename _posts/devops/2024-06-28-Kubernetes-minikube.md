---
title:  "Kubernetes"
date:   2024-06-28 11:02:00
categories: ["DevOps","GitOps"]
tags: ["DevOps","GitOps"]
---

{% include toc title="Index" %}

An Open source Container Orchestration platform

Automates

- Deployment of containers
- Scaling of containers
- Maintenance of containers

![k8s_cluster_small.png]({{ site.url }}/assets/images/k8s_cluster_small.png)

[https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#what-is-k8s-kubernetes](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#what-is-k8s-kubernetes)

![](https://www.youtube.com/watch?v=TlHvYWVUZyc)

# Minikube

[https://minikube.sigs.k8s.io/docs/handbook/controls/](https://minikube.sigs.k8s.io/docs/handbook/controls/)

```shell
brew install minikube
```

Start/shutdown the cluster

```shell
minikube start
minikube stop # Saves the state
minikube delete # Deletes everything
```

Dashboard

```shell
minikube dashboard
```

# K8S - Important Commands

Create a namespace

```shell
kubectl create ns non-prod
```

Check running pod

```shell
#IpAddress, port, clusterId etc
kubectl get service

# Get podname, status
kubectl get pods # podname from minikube dashboard can also be used

#Get details like IP addres, status
kubectl describe pod <pod_name>
kubectl describe pod todo-service-app-todo-app-7b45c8749b-ltmfw


```

### Access from Another Pod

use a temporary pod to check if the application is reachable from within the
cluster

`-i -t` flag Allows us to provide input to the container

```shell
kubectl run -it --rm --restart=Never busybox --image=busybox -- sh
```

Then, inside the busybox shell, try to curl your application:

```shell
wget -qO- http://<your-pod-ip>:<port-number>/actuator/health

wget -qO- http://10.109.198.72:5000/actuator/health
```

### Check Resource Usage

```shell
kubectl top pod <pod-name>
kubectl top pod todo-service-app-todo-app-7b45c8749b-ltmfw
```

### Check Application logs

```shell
kubectl logs <pod-name>
kubectl logs todo-service-app-todo-app-7b45c8749b-ltmfw

# Running log
kubectl logs -f todo-service-app-todo-app-7b45c8749b-ltmfw
```