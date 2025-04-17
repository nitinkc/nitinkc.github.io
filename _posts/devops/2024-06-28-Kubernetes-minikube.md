---
title:  "Kubernetes Commands"
date: 2025-04-11 05:00:00
categories: ["DevOps","GitOps"]
tags: ["DevOps","GitOps"]
---

{% include toc title="Index" %}

Automates
- Deployment of containers
- Scaling of containers
- Maintenance of containers

![k8s_cluster_architecture.png]({{ site.url }}/assets/images/k8s_cluster_architecture.png){:width="25%"}

![k8s_cluster_small.png]({{ site.url }}/assets/images/k8s_cluster_small.png)

[what-is-k8s-kubernetes](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#what-is-k8s-kubernetes)

![](https://www.youtube.com/watch?v=TlHvYWVUZyc)

# Minikube
[Minikube Basic controls](https://minikube.sigs.k8s.io/docs/handbook/controls/)

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

# Create a namespace
```shell
kubectl create ns non-prod
```

# Shell redirection to connect to a Pod
```shell
kubectl exec -it new-nginx -- /bin/bash
```

### Access from Another Pod
use a temporary pod to check if the application is reachable from within the
cluster
- `-i -t` flag Allows us to provide input to the container
```shell
kubectl run -it --rm --restart=Never busybox --image=busybox -- sh
```

Then, inside the busybox shell, try to curl your application:
```shell
wget -qO- http://<your-pod-ip>:<port-number>/actuator/health

wget -qO- http://10.109.198.72:5000/actuator/health
```

# Debugs & Checks 
use autocomplete (for GCP Cloud shell)
```shell
source <(kubectl completion bash)
```

### Pod related commands
```shell
# Get podname, status
kubectl get pods # podname from minikube dashboard can also be used
export my_pod=[your_pod_name]

#Get details like IP addres, status
kubectl describe pod $my_pod

# Services - #IpAddress, port, clusterId etc
kubectl get service nginx
```

### Deployment related
```shell
# Deployment related
kubectl get deployments

# the rollout history of the deployment:
kubectl rollout history deployment nginx-deployment
```

### Check Resource Usage
```shell
# to view the resource usage across the nodes of the cluster
kubectl top node

# view the resources being used by the Pod:
kubectl top pods

# Check particular pod
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

### Cluster config
```shell
kubectl config view
kubectl cluster-info
kubectl config current-context
kubectl config get-contexts

#  command to change the active context:
kubectl config use-context gke_${DEVSHELL_PROJECT_ID}_Region_autopilot-cluster-1
source <(kubectl completion bash)
```
