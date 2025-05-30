---
title: "Kubernetes Concepts"
date: 2025-04-29 05:00:00
categories: [ DevOps ]
tags: [ DevOps ]
---
{% include toc title="Index" %}

# Pods Vs Container

**Container:** A lightweight, standalone, **executable package** that includes everything needed to run a piece of software, including 
- the code, 
- runtime, 
- libraries, and 
- dependencies.

Containers are isolated from each other and the host system.

**Pod:** The smallest deployable unit in Kubernetes, a pod can **contain one or more containers**. 
- Pods share the same network namespace, meaning they can communicate with each other using `localhost`.

### **IP Address and Port:**
**Container:**
  - Each container typically gets its own IP address when running in a **non-Kubernetes** environment.
  - Containers can expose ports to allow external access to the services they run.

**Pod:**
- In Kubernetes, each pod gets a **unique IP address** within the cluster.
- Pods have a single IP address shared by all containers within the pod.
- Containers within the same pod share the same network namespace, IP address, and port space. 
  - They can communicate with each other directly via `localhost` and **do not need to expose ports** to communicate **internally**.

##### Example:
Imagine a pod with two containers:
- Container A runs a web server on port 80.
- Container B runs a database server on port 5432.

Both containers can communicate with each other using localhost, and they share the pod's IP address. 

External services can access the web server via the pod's IP address and port 80, and the database server via the pod's IP address and port 5432.

# Kubernetes Architecture

[https://kubernetes.io/docs/concepts/architecture/](https://kubernetes.io/docs/concepts/architecture/)

![](https://kubernetes.io/images/docs/kubernetes-cluster-architecture.svg){:width="70%" height="50%"}

# **Deployment**
A deployment manages the **creation and updating of instances** of your application (**pods**).
  - It ensures that the desired number of pod replicas are running at all times.
  - Kubernetes  handles the rollout and scaling of these pods.

**Example**: If you have a Spring Boot application, you would create a deployment to ensure multiple instances of
your application are running for high availability.

### Deployment YAML
- **apiVersion**: Specifies the API version.
- **kind**: Defines the type of Kubernetes object, which is a Deployment.
- **metadata**: Contains the name of the deployment.
- **spec**: Defines the desired state of the deployment.
  - **replicas**: Specifies the number of pod replicas.
  - **selector**: Matches the pods with the label `app: springboot`.
  - **template**: Describes the pods to be created.
    - **metadata**: Labels the pods.
    - **spec**: Defines the container specifications.
      - **containers**: Lists the containers in the pod.
        - **name**: Names the container.
        - **image**: Specifies the container image.
        - **ports**: Defines the container port.


`deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: springboot-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: springboot
  template:
    metadata:
      labels:
        app: springboot
    spec:
      containers:
      - name: springboot-container
        image: nitinkc/k8s-helloworld:k8s-hw-v6
        ports:
        - containerPort: 8080

```

# **Types of Services:**

> The correct URL to access the application can be found by the `minikube service springboot-service --url` command.
> Access the Service: Open your browser and navigate to http://NodeIP:NodePort

##### Service YAML
- **apiVersion**: Specifies the API version.
- **kind**: Defines the type of Kubernetes object, which is a Service.
- **metadata**: Contains the name of the service.
- **spec**: Defines the desired state of the service.
  - **selector**: Matches the pods with the label `app: springboot`.
  - **ports**: Defines the service ports.
    - **protocol**: Specifies the protocol (TCP).
    - **port**: Defines the port on which the service is exposed.
    - **targetPort**: Specifies the port on the container to which traffic should be directed.

### **ClusterIP (default):**
Exposes the service on an internal IP within the cluster. This type of service is only accessible from within the cluster.
- **Use Case:** Ideal for internal communication between services within the cluster.
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: springboot-service
  spec:
    selector:
      app: springboot
    ports:
      - protocol: TCP
        port: 80
        targetPort: 8080
    type: ClusterIP
  ```

### **NodePort:**
NodePort: Exposes the application on a specific port on each Node.

Exposes the service on each Node's IP at a static port (the NodePort). This makes the service accessible from outside the cluster using `<NodeIP>:<NodePort>`.
- **Use Case:** Useful for exposing services for external access during development or testing.
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: springboot-service
    spec:
      selector:
        app: springboot
      ports:
        - protocol: TCP
          port: 80
          targetPort: 8080
          nodePort: 30007
      type: NodePort
    ```

### **LoadBalancer:**
LoadBalancer: Provides an external IP and port, accessible via minikube tunnel.

**Creates an external load balancer** (if supported by the cloud provider) and assigns a fixed, external IP to the service. 
- A service provides **a stable endpoint** to access your pods from outside the cluster.
  - It abstracts away the details of the pods and provides a consistent way to access them, even as pods are created and destroyed.
  - YAML file specifies the type (e.g., ClusterIP, NodePort, LoadBalancer), the selector to match pods, and the port to expose.

**Example**: If your Spring Boot application needs to be accessible from outside the cluster, you would create a service
to expose it, allowing users to interact with your application.

- **Use Case:** Ideal for production environments where you need to expose services to the internet.
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: springboot-service
    spec:
      selector:
        app: springboot
      ports:
        - protocol: TCP
          port: 80
          targetPort: 8080
      type: LoadBalancer
    ```

### **ExternalName:**
Maps a service to a DNS name by returning a CNAME record with the specified external name. This type of service does not use selectors.
- **Use Case:** Useful for integrating with external services that are not part of the Kubernetes cluster.
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: external-service
  spec:
    type: ExternalName
    externalName: my.external.service.com
  ```

## **Summary:**
- **ClusterIP:** Internal access within the cluster.
- **NodePort:** External access via `<NodeIP>:<NodePort>`.
- **LoadBalancer:** External access via a cloud provider's load balancer.
- **ExternalName:** Maps to an external DNS name.


```shell
# Find the NodePort
kubectl get service springboot-service
kubectl get endpoints springboot-service

# Get the Node IP:
minikube ip

# Inspect Pod Health and Readiness:
kubectl get pods
kubectl describe pod <pod-name>

# Test Connectivity from Within the Cluster
kubectl run -it --rm --restart=Never busybox --image=gcr.io/google-containers/busybox sh
wget -qO- http://<pod-ip>:8080

# Inspect Logs
kubectl logs <pod-name>

```
