---
categories: DevOps
date: 2025-04-29 05:00:00
tags:
- Kubernetes
- DevOps
title: Kubernetes on Google Kubernetes Engine (GKE)
---

{% include toc title="Index" %}

# Code and Help
[Kubernetes & Springboot HelloWorld](https://github.com/nitinkc/K8SHelloWorld)

# Create a cluster
### Via Shell
```shell
gcloud beta container \
--project "playground-s-11-7221e07f" \
clusters create-auto "autopilot-cluster-1" \
--region "us-central1" \
--release-channel "regular" \
--tier "standard"\
--enable-dns-access \
--enable-ip-access --no-enable-google-cloud-access --network "projects/playground-s-11-7221e07f/global/networks/default"\
--subnetwork "projects/playground-s-11-7221e07f/regions/us-central1/subnetworks/default" \
--cluster-ipv4-cidr "/21"\
--binauthz-evaluation-mode=DISABLED \
--enable-ray-operator \
--enable-dataplane-v2-flow-observability \
--enable-secret-manager
```

### Via UI
```shell
export my_region=us-east4
export my_cluster=autopilot-cluster-1

source <(kubectl completion bash)

# Create a cluster
# https://cloud.google.com/sdk/gcloud/reference/container/clusters/create
gcloud container clusters create-auto $my_cluster --region $my_region

# Connect to a GKE cluster
gcloud container clusters get-credentials $my_cluster --region $my_region
# This command creates a .kube directory in your home directory if it doesn't already exist. 
# In the .kube directory, the command creates a file named config if it doesn't already exist,
# which is used to store the authentication and configuration information.
# The config file is typically called the kubeconfig file.
```

### Check 
```shell
kubectl config view
kubectl cluster-info
kubectl config current-context
kubectl config get-contexts

#  command to change the active context:
kubectl config use-context gke_${DEVSHELL_PROJECT_ID}_Region_autopilot-cluster-1
source <(kubectl completion bash)
```

# Create a deployment
```shell
kubectl create deployment --image nginx nginx-1
# creates a Pod named nginx with a container running the nginx image. When a repository isn't specified, 
# the default behavior is to try to find the image either locally or in the Docker public registry.
```

# Deployment on GKE
`nginx-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

Deploy using the file
```shell
kubectl apply -f ./nginx-deployment.yaml
# Check status
kubectl get deployments
```

# Push a file to a container
```shell
kubectl cp ~/test.html $my_pod:/usr/share/nginx/html/test.html
# copies the test.html file from the local home directory to the /usr/share/nginx/html directory of the first container 
# in the nginx Pod. You can specify other containers in a multi-container Pod by using the -c option, 
# followed by the name of the container.
```

# Expose a pod for testing
```shell
# creates a LoadBalancer service, which allows the nginx Pod to be accessed 
# from internet addresses outside of the cluster
kubectl expose pod $my_pod --port 80 --type LoadBalancer

kubectl get services

curl http://[EXTERNAL_IP]/test.html
```

# Scale Pods up and down in the shell
```shell
kubectl scale --replicas=3 deployment nginx-deployment
```

# Trigger a deployment rollout

```shell
# To update the version of nginx in the deployment:
kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.9.1 
# updates the container image in your Deployment to nginx v1.9.1

# annotate the rollout with details on the change
kubectl annotate deployment nginx-deployment kubernetes.io/change-cause="version change to 1.9.1" --overwrite=true

# view the rollout status
kubectl rollout status deployment.v1.apps/nginx-deployment

# the rollout history of the deployment:
kubectl rollout history deployment nginx-deployment
```

# Trigger a deployment rollback

```shell
# roll back to the previous version of the nginx deployment
kubectl rollout undo deployments nginx-deployment

# the rollout history of the deployment:
kubectl rollout history deployment nginx-deployment

# View the details of the latest deployment revision
kubectl rollout history deployment/nginx-deployment --revision=3
```

# Define service types in the manifest

### Kind : Pods

The preferred way of deploying Pods and other resources to Kubernetes is **_through configuration files_**, 
which are sometimes called _**manifest files_**.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: new-nginx
  labels:
    name: new-nginx
spec:
  containers:
  - name: new-nginx
    image: nginx
    ports:
    - containerPort: 80
```

To deploy your manifest, execute the following command:

set up port forwarding from Cloud Shell to the nginx Pod (from port 10081 of the Cloud Shell VM to port 80 of the nginx container
```shell
kubectl apply -f ./new-nginx-pod.yaml
```

#
```shell
kubectl port-forward new-nginx 10081:80
```

### Kind : Service
service-nginx.yaml
{% gist nitinkc/81a87ef5084c8c83a355634f2623e035%}


# Perform a canary deployment

### Kind : Deployment

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

Create the canary deployment based on the configuration file
```shell
kubectl apply -f ./nginx-canary.yaml
kubectl get deployments
```
Scale down
```shell
kubectl scale --replicas=0 deployment nginx-deployment
```

# Session affinity
Set the sessionAffinity field to ClientIP in the specification of the service if you need a client's first request to
determine which Pod will be used for all subsequent connections
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  type: LoadBalancer
  sessionAffinity: ClientIP
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 60000
    targetPort: 80
```
# Deploy a Springboot app

Springboot application runs on port 5000(resources.yaml). Load balancer should allow only port 8080
```shell
kubectl create deployment hello-service \
        --image=gcr.io/my-kubernetes-project-52188/hello-world:v1

kubectl expose deployment hello-service \
        --type=LoadBalancer --port=8080 --target-port=5000
```

### Subsequent deployments
```shell
kubectl set image deployment/hello-service hello-service=\
dockerhub-username/image-name:new-tag
```

### Manually scale up and down the number of Pods in deployments
```shell
kubectl scale deployment hello-capgemini-service --replicas=5
```