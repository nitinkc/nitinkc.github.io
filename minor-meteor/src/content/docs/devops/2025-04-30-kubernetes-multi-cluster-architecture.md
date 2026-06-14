---
title: "Kubernetes Multi-Cluster Architecture: East-West Region Setup"
date: 2025-04-30 05:00:00
categories:
- DevOps
tags:
- Kubernetes
- Multi-Cluster
- Service Mesh
- High Availability
---

{% include toc title="Index" %}

# Multi-Cluster Architecture Overview

This guide demonstrates a production-grade multi-cluster Kubernetes setup with two regional clusters (East and West) for high availability, disaster recovery, and geographic load distribution.

![](https://raw.githubusercontent.com/kubernetes/website/main/static/images/docs/kubernetes-cluster-architecture.svg)

# Architecture Design

## Scenario: E-Commerce Platform with Multi-Region Deployment

We'll build an e-commerce application with:
- **East Cluster (us-east-1)**: Primary region serving East Coast users
- **West Cluster (us-west-1)**: Secondary region serving West Coast users
- **Services**: Frontend, Product Service, Order Service, Inventory Service, Shared Database
- **Traffic Management**: Geographic routing, failover, and load balancing

```
┌─────────────────────────────────────────────────────────────────┐
│                       Global Load Balancer                       │
│                    (Route53 / CloudFlare)                       │
└────────────────┬────────────────────────────────┬───────────────┘
                 │                                │
        ┌────────▼─────────┐            ┌────────▼─────────┐
        │  East Cluster    │            │  West Cluster    │
        │  (us-east-1)     │◄──────────►│  (us-west-1)     │
        └──────────────────┘            └──────────────────┘
           │    │    │                      │    │    │
           │    │    └── Inventory          │    │    └── Inventory
           │    └────── Order Service       │    └────── Order Service
           └────────── Product Service      └────────── Product Service
```

# Prerequisites

```shell
# Install required tools
brew install kubectl kubectx istioctl helm

# Install kind for local multi-cluster testing
brew install kind

# Install kubectl plugins
kubectl krew install ctx ns
```

# Setting Up Multi-Cluster Environment

## Option 1: Local Development with Kind

Create two local clusters to simulate East and West regions:

```shell
# Create East cluster
cat <<EOF | kind create cluster --name east-cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 30080
  - containerPort: 30443
    hostPort: 30443
- role: worker
- role: worker
EOF

# Create West cluster
cat <<EOF | kind create cluster --name west-cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30081
    hostPort: 30081
  - containerPort: 30444
    hostPort: 30444
- role: worker
- role: worker
EOF
```

## Option 2: Cloud Clusters (GKE Example)

```shell
# Create East cluster on GKE
gcloud container clusters create east-cluster \
  --zone=us-east1-b \
  --num-nodes=3 \
  --machine-type=e2-standard-4 \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=5

# Create West cluster on GKE
gcloud container clusters create west-cluster \
  --zone=us-west1-a \
  --num-nodes=3 \
  --machine-type=e2-standard-4 \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=5

# Get credentials
gcloud container clusters get-credentials east-cluster --zone=us-east1-b
gcloud container clusters get-credentials west-cluster --zone=us-west1-a
```

## Verify Cluster Contexts

```shell
# List all contexts
kubectl config get-contexts

# Rename contexts for clarity
kubectl config rename-context kind-east-cluster east
kubectl config rename-context kind-west-cluster west

# Switch between clusters
kubectx east  # or: kubectl config use-context east
kubectx west  # or: kubectl config use-context west

# Check current context
kubectx -c
```

# Deploy Namespace and Resources

## Create Namespaces in Both Clusters

```shell
# Create namespaces in East cluster
kubectx east
kubectl create namespace ecommerce
kubectl create namespace monitoring
kubectl create namespace istio-system

# Create namespaces in West cluster
kubectx west
kubectl create namespace ecommerce
kubectl create namespace monitoring
kubectl create namespace istio-system

# Label namespaces for Istio injection
kubectl label namespace ecommerce istio-injection=enabled --context=east
kubectl label namespace ecommerce istio-injection=enabled --context=west
```

# Application Deployment

## 1. Product Service (Stateless - Both Clusters)

`product-service/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service
  namespace: ecommerce
  labels:
    app: product-service
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: product-service
  template:
    metadata:
      labels:
        app: product-service
        version: v1
    spec:
      containers:
      - name: product-service
        image: nitinkc/product-service:v1.0
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "production"
        - name: REGION
          valueFrom:
            fieldRef:
              fieldPath: metadata.labels['topology.kubernetes.io/region']
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: product-service
  namespace: ecommerce
  labels:
    app: product-service
spec:
  type: ClusterIP
  selector:
    app: product-service
  ports:
  - name: http
    port: 8080
    targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: product-service-hpa
  namespace: ecommerce
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: product-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 2. Order Service (Stateful - Primary in East, Replica in West)

`order-service/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: order-service
  namespace: ecommerce
spec:
  serviceName: order-service
  replicas: 2
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
      - name: order-service
        image: nitinkc/order-service:v1.0
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: KAFKA_BROKERS
          value: "kafka-0.kafka-headless.ecommerce.svc.cluster.local:9092"
        volumeMounts:
        - name: order-data
          mountPath: /data
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
  volumeClaimTemplates:
  - metadata:
      name: order-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: ecommerce
spec:
  clusterIP: None
  selector:
    app: order-service
  ports:
  - name: http
    port: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: order-service-lb
  namespace: ecommerce
spec:
  type: LoadBalancer
  selector:
    app: order-service
  ports:
  - name: http
    port: 80
    targetPort: 8080
```

## 3. Inventory Service (Shared State with Redis)

`inventory-service/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: inventory-service
  namespace: ecommerce
spec:
  replicas: 2
  selector:
    matchLabels:
      app: inventory-service
  template:
    metadata:
      labels:
        app: inventory-service
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - inventory-service
              topologyKey: kubernetes.io/hostname
      containers:
      - name: inventory-service
        image: nitinkc/inventory-service:v1.0
        ports:
        - containerPort: 8080
        env:
        - name: REDIS_HOST
          value: "redis-master.ecommerce.svc.cluster.local"
        - name: REDIS_PORT
          value: "6379"
        - name: CACHE_ENABLED
          value: "true"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: inventory-service
  namespace: ecommerce
spec:
  type: ClusterIP
  selector:
    app: inventory-service
  ports:
  - port: 8080
    targetPort: 8080
```

## 4. Frontend Service (Ingress with Geographic Routing)

`frontend/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: ecommerce
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: nitinkc/ecommerce-frontend:v1.0
        ports:
        - containerPort: 3000
        env:
        - name: PRODUCT_SERVICE_URL
          value: "http://product-service.ecommerce.svc.cluster.local:8080"
        - name: ORDER_SERVICE_URL
          value: "http://order-service-lb.ecommerce.svc.cluster.local"
        - name: INVENTORY_SERVICE_URL
          value: "http://inventory-service.ecommerce.svc.cluster.local:8080"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: ecommerce
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
  - name: http
    port: 80
    targetPort: 3000
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: frontend-ingress
  namespace: ecommerce
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - ecommerce.example.com
    secretName: frontend-tls
  rules:
  - host: ecommerce.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

# Deploy to Both Clusters

```shell
# Deploy to East cluster
kubectx east
kubectl apply -f product-service/deployment.yaml
kubectl apply -f order-service/deployment.yaml
kubectl apply -f inventory-service/deployment.yaml
kubectl apply -f frontend/deployment.yaml

# Deploy to West cluster
kubectx west
kubectl apply -f product-service/deployment.yaml
kubectl apply -f order-service/deployment.yaml
kubectl apply -f inventory-service/deployment.yaml
kubectl apply -f frontend/deployment.yaml

# Verify deployments
kubectl get all -n ecommerce --context=east
kubectl get all -n ecommerce --context=west
```

# Advanced Configurations

## ConfigMap for Multi-Region Settings

`configs/configmap.yaml`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: region-config
  namespace: ecommerce
data:
  # East cluster config
  east.properties: |
    region=us-east-1
    primary=true
    peer.region=us-west-1
    peer.endpoint=https://west-cluster.example.com
    
  # West cluster config
  west.properties: |
    region=us-west-1
    primary=false
    peer.region=us-east-1
    peer.endpoint=https://east-cluster.example.com
```

## Secrets Management

```shell
# Create database credentials in East cluster
kubectl create secret generic db-credentials \
  --from-literal=url='jdbc:postgresql://east-db.example.com:5432/orders' \
  --from-literal=username='orderuser' \
  --from-literal=password='secretpassword123' \
  --namespace=ecommerce \
  --context=east

# Create database credentials in West cluster
kubectl create secret generic db-credentials \
  --from-literal=url='jdbc:postgresql://west-db.example.com:5432/orders' \
  --from-literal=username='orderuser' \
  --from-literal=password='secretpassword123' \
  --namespace=ecommerce \
  --context=west
```

## Network Policies

`network-policies/product-service-policy.yaml`
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: product-service-policy
  namespace: ecommerce
spec:
  podSelector:
    matchLabels:
      app: product-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    - podSelector:
        matchLabels:
          app: order-service
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 53
  - to:
    - podSelector:
        matchLabels:
          app: inventory-service
    ports:
    - protocol: TCP
      port: 8080
```

Apply network policies:
```shell
kubectl apply -f network-policies/ --context=east
kubectl apply -f network-policies/ --context=west
```

# Cross-Cluster Service Discovery

## Using Istio for Multi-Cluster Mesh

Install Istio in both clusters:

```shell
# Install Istio in East cluster
kubectx east
istioctl install --set profile=demo -y

# Install Istio in West cluster
kubectx west
istioctl install --set profile=demo -y
```

## ServiceEntry for Cross-Cluster Communication

`istio/service-entry.yaml`
```yaml
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: west-product-service
  namespace: ecommerce
spec:
  hosts:
  - product-service.west.global
  location: MESH_INTERNAL
  ports:
  - number: 8080
    name: http
    protocol: HTTP
  resolution: DNS
  endpoints:
  - address: west-cluster-lb.example.com
    ports:
      http: 8080
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: product-service-circuit-breaker
  namespace: ecommerce
spec:
  host: product-service.ecommerce.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

# Monitoring and Observability

## Prometheus Configuration

`monitoring/prometheus-config.yaml`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
      external_labels:
        cluster: 'east-cluster'
        region: 'us-east-1'
    
    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

Deploy Prometheus using Helm:
```shell
# Add Prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install in East cluster
kubectx east
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.externalLabels.cluster=east-cluster

# Install in West cluster
kubectx west
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.externalLabels.cluster=west-cluster
```

# Load Testing and Validation

## Generate Load

```shell
# Install k6 for load testing
brew install k6

# Create load test script
cat > load-test.js << 'EOF'
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '2m', target: 0 },
  ],
};

export default function () {
  let response = http.get('http://ecommerce.example.com/api/products');
  check(response, { 'status was 200': (r) => r.status == 200 });
  sleep(1);
}
EOF

# Run load test
k6 run load-test.js
```

## Monitor Both Clusters

```shell
# Watch pods in both clusters
watch -n 2 'echo "=== EAST CLUSTER ===" && kubectl get pods -n ecommerce --context=east && echo "\n=== WEST CLUSTER ===" && kubectl get pods -n ecommerce --context=west'

# Check HPA scaling
kubectl get hpa -n ecommerce --context=east -w
kubectl get hpa -n ecommerce --context=west -w

# View resource usage
kubectl top pods -n ecommerce --context=east
kubectl top pods -n ecommerce --context=west

# Check service endpoints
kubectl get endpoints -n ecommerce --context=east
kubectl get endpoints -n ecommerce --context=west
```

# Disaster Recovery Scenarios

## Simulate East Cluster Failure

```shell
# Scale down all deployments in East cluster
kubectx east
kubectl scale deployment --all --replicas=0 -n ecommerce

# Verify West cluster handles traffic
kubectx west
kubectl get pods -n ecommerce
kubectl logs -f deployment/product-service -n ecommerce

# Restore East cluster
kubectx east
kubectl scale deployment product-service --replicas=3 -n ecommerce
kubectl scale deployment inventory-service --replicas=2 -n ecommerce
kubectl scale deployment frontend --replicas=3 -n ecommerce
```

## Database Failover

```shell
# Promote West database to primary
kubectl exec -it order-service-0 -n ecommerce --context=west -- \
  psql -U orderuser -d orders -c "SELECT pg_promote();"

# Update order service to use West database
kubectl set env statefulset/order-service \
  DATABASE_URL='jdbc:postgresql://west-db.example.com:5432/orders' \
  -n ecommerce --context=west
```

# Best Practices Demonstrated

1. **High Availability**: Multiple replicas across zones and regions
2. **Horizontal Scaling**: HPA based on CPU and memory metrics
3. **Circuit Breaking**: Istio DestinationRules for fault tolerance
4. **Resource Management**: Proper requests and limits
5. **Health Checks**: Liveness and readiness probes
6. **Security**: Network policies, secrets management
7. **Observability**: Prometheus metrics, centralized logging
8. **StatefulSet**: For order service with persistent storage
9. **Anti-Affinity**: Spread pods across nodes
10. **Multi-Cluster**: Cross-cluster service discovery and failover

# Cleanup

```shell
# Delete resources from both clusters
kubectx east
kubectl delete namespace ecommerce monitoring

kubectx west
kubectl delete namespace ecommerce monitoring

# Delete local kind clusters
kind delete cluster --name east-cluster
kind delete cluster --name west-cluster

# Delete GKE clusters (if using cloud)
gcloud container clusters delete east-cluster --zone=us-east1-b --quiet
gcloud container clusters delete west-cluster --zone=us-west1-a --quiet
```

# Summary

This multi-cluster setup demonstrates:
- **Geographic Distribution**: East and West clusters for low latency
- **High Availability**: Redundant services across regions
- **Load Balancing**: Automatic traffic distribution
- **Service Mesh**: Istio for advanced traffic management
- **Monitoring**: Prometheus and Grafana for observability
- **Disaster Recovery**: Failover capabilities between clusters
- **Scaling**: HPA for automatic pod scaling
- **Security**: Network policies and secrets management

This architecture provides a production-ready foundation for running distributed applications across multiple Kubernetes clusters.

