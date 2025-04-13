---
title: "Kubernetes k8s Commands"
date: 2025-04-11 05:00:00
categories: [ GCP ]
tags: [ GCP ]
---



```shell

export my_region=us-east4
export my_cluster=autopilot-cluster-1

source <(kubectl completion bash)


gcloud container clusters get-credentials $my_cluster --region $my_region

kubectl apply -f ./nginx-deployment.yaml

kubectl get deployments


```

# Scale Pods up and down in the shell
```shell
kubectl scale --replicas=3 deployment nginx-deployment
```

# Trigger a deployment rollout


```shell
kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.9.1 

kubectl annotate deployment nginx-deployment kubernetes.io/change-cause="version change to 1.9.1" --overwrite=true

kubectl rollout status deployment.v1.apps/nginx-deployment

kubectl rollout history deployment nginx-deployment
```

#

```shell
kubectl rollout undo deployments nginx-deployment

kubectl rollout history deployment nginx-deployment

kubectl rollout history deployment/nginx-deployment --revision=3
```

# Define service types in the manifest

service-nginx.yaml
```shell
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 60000
    targetPort: 80
```


# Perform a canary deployment

nano nginx-canary.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-canary
  labels:
    app: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
        track: canary
        Version: 1.9.1
    spec:
      containers:
      - name: nginx
        image: nginx:1.9.1
        ports:
        - containerPort: 80
```

```shell
kubectl apply -f ./nginx-canary.yaml
kubectl get deployments

kubectl scale --replicas=0 deployment nginx-deployment
```