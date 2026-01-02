---
title: "Kubernetes Hands-On: Building a Multi-Region E-Commerce Platform"
date: 2025-04-30 07:00:00
categories:
- DevOps
tags:
- Kubernetes
- Tutorial
- Hands-On
- Multi-Cluster
---

{% include toc title="Index" %}

# Complete Hands-On Tutorial

This is a step-by-step practical guide to deploy a realistic multi-region e-commerce platform with East and West clusters. Follow along to gain hands-on experience with advanced Kubernetes concepts.

# Lab Setup

## Prerequisites Checklist

```shell
# Verify installations
docker --version
kubectl version --client
kind --version
helm version

# Install missing tools on macOS
brew install kubectl kind helm kubectx k9s stern
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Global DNS Load Balancer                  │
└────────────────┬───────────────────────────┬─────────────────┘
                 │                           │
         ┌───────▼────────┐          ┌──────▼──────────┐
         │  East Cluster  │          │  West Cluster   │
         │  (Primary)     │◄────────►│  (Secondary)    │
         └────────────────┘          └─────────────────┘
              │                              │
         ┌────┴────┐                    ┌────┴────┐
         │ Frontend│                    │ Frontend│
         │ Product │                    │ Product │
         │ Order   │                    │ Order   │
         │ Inventory                   │ Inventory
         └─────────┘                    └─────────┘
```

# Step 1: Create Multi-Cluster Environment

## Create East Cluster

```shell
cat <<EOF | kind create cluster --name east-cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  podSubnet: "10.240.0.0/16"
  serviceSubnet: "10.241.0.0/16"
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "region=us-east-1,zone=us-east-1a"
  extraPortMappings:
  - containerPort: 30080
    hostPort: 8080
    protocol: TCP
  - containerPort: 30081
    hostPort: 8081
    protocol: TCP
- role: worker
  kubeadmConfigPatches:
  - |
    kind: JoinConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "region=us-east-1,zone=us-east-1a"
- role: worker
  kubeadmConfigPatches:
  - |
    kind: JoinConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "region=us-east-1,zone=us-east-1b"
EOF

echo "✓ East cluster created successfully"
```

## Create West Cluster

```shell
cat <<EOF | kind create cluster --name west-cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  podSubnet: "10.242.0.0/16"
  serviceSubnet: "10.243.0.0/16"
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "region=us-west-1,zone=us-west-1a"
  extraPortMappings:
  - containerPort: 30080
    hostPort: 9080
    protocol: TCP
  - containerPort: 30081
    hostPort: 9081
    protocol: TCP
- role: worker
  kubeadmConfigPatches:
  - |
    kind: JoinConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "region=us-west-1,zone=us-west-1a"
- role: worker
  kubeadmConfigPatches:
  - |
    kind: JoinConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "region=us-west-1,zone=us-west-1b"
EOF

echo "✓ West cluster created successfully"
```

## Configure Contexts

```shell
# Rename contexts for clarity
kubectl config rename-context kind-east-cluster east
kubectl config rename-context kind-west-cluster west

# Verify contexts
kubectl config get-contexts

# Test switching
kubectx east && kubectl get nodes
kubectx west && kubectl get nodes

echo "✓ Cluster contexts configured"
```

# Step 2: Create Namespaces and Labels

```shell
# Function to setup namespace
setup_namespace() {
  local context=$1
  kubectx $context
  
  kubectl create namespace ecommerce
  kubectl create namespace monitoring
  kubectl create namespace ingress-nginx
  
  kubectl label namespace ecommerce \
    environment=production \
    region=$context \
    managed-by=hands-on-lab
  
  echo "✓ Namespaces created in $context cluster"
}

# Setup both clusters
setup_namespace east
setup_namespace west
```

# Step 3: Deploy NGINX Ingress Controller

```shell
deploy_ingress() {
  local context=$1
  kubectx $context
  
  kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
  
  echo "Waiting for ingress controller to be ready in $context..."
  kubectl wait --namespace ingress-nginx \
    --for=condition=ready pod \
    --selector=app.kubernetes.io/component=controller \
    --timeout=90s
  
  echo "✓ Ingress controller ready in $context"
}

deploy_ingress east
deploy_ingress west
```

# Step 4: Deploy Redis for Shared Cache

Create Redis StatefulSet:

```shell
cat > redis-statefulset.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: redis-headless
  namespace: ecommerce
spec:
  clusterIP: None
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: redis
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: ecommerce
spec:
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: redis
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: ecommerce
spec:
  serviceName: redis-headless
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
          name: redis
        command:
        - redis-server
        - --appendonly
        - "yes"
        volumeMounts:
        - name: redis-data
          mountPath: /data
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
  volumeClaimTemplates:
  - metadata:
      name: redis-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
EOF

# Deploy to both clusters
kubectx east && kubectl apply -f redis-statefulset.yaml
kubectx west && kubectl apply -f redis-statefulset.yaml

# Verify Redis is running
kubectx east && kubectl wait --for=condition=ready pod -l app=redis -n ecommerce --timeout=120s
kubectx west && kubectl wait --for=condition=ready pod -l app=redis -n ecommerce --timeout=120s

echo "✓ Redis deployed to both clusters"
```

# Step 5: Deploy Product Service

```shell
cat > product-service.yaml <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: product-service-config
  namespace: ecommerce
data:
  application.yaml: |
    server:
      port: 8080
    spring:
      application:
        name: product-service
      redis:
        host: redis
        port: 6379
    management:
      endpoints:
        web:
          exposure:
            include: health,info,metrics,prometheus
---
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
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/actuator/prometheus"
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
                  - product-service
              topologyKey: kubernetes.io/hostname
      containers:
      - name: product-service
        image: hashicorp/http-echo:0.2.3
        args:
        - "-text=Product Service v1 - Region: $(REGION)"
        - "-listen=:8080"
        env:
        - name: REGION
          valueFrom:
            fieldRef:
              fieldPath: metadata.labels['topology.kubernetes.io/region']
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: REDIS_HOST
          value: redis
        ports:
        - containerPort: 8080
          name: http
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 8080
          initialDelaySeconds: 5
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
  ports:
  - port: 8080
    targetPort: 8080
    name: http
  selector:
    app: product-service
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
EOF

# Deploy to both clusters
kubectx east && kubectl apply -f product-service.yaml
kubectx west && kubectl apply -f product-service.yaml

# Verify deployment
kubectx east && kubectl rollout status deployment/product-service -n ecommerce
kubectx west && kubectl rollout status deployment/product-service -n ecommerce

echo "✓ Product service deployed to both clusters"
```

# Step 6: Deploy Order Service (StatefulSet)

```shell
cat > order-service.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: order-service-headless
  namespace: ecommerce
spec:
  clusterIP: None
  ports:
  - port: 8080
    name: http
  selector:
    app: order-service
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: ecommerce
spec:
  type: NodePort
  ports:
  - port: 8080
    targetPort: 8080
    nodePort: 30081
    name: http
  selector:
    app: order-service
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: order-service
  namespace: ecommerce
spec:
  serviceName: order-service-headless
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
        image: hashicorp/http-echo:0.2.3
        args:
        - "-text=Order Service - Pod: $(POD_NAME) - Region: $(REGION)"
        - "-listen=:8080"
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: REGION
          valueFrom:
            fieldRef:
              fieldPath: metadata.labels['topology.kubernetes.io/region']
        ports:
        - containerPort: 8080
          name: http
        volumeMounts:
        - name: order-data
          mountPath: /data
        resources:
          requests:
            cpu: 200m
            memory: 256Mi
          limits:
            cpu: 1000m
            memory: 1Gi
  volumeClaimTemplates:
  - metadata:
      name: order-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
EOF

# Deploy to both clusters
kubectx east && kubectl apply -f order-service.yaml
kubectx west && kubectl apply -f order-service.yaml

# Wait for StatefulSet to be ready
kubectx east && kubectl rollout status statefulset/order-service -n ecommerce
kubectx west && kubectl rollout status statefulset/order-service -n ecommerce

echo "✓ Order service deployed to both clusters"
```

# Step 7: Deploy Frontend with Ingress

```shell
cat > frontend.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: ecommerce
spec:
  replicas: 2
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
        image: nginxdemos/hello:plain-text
        ports:
        - containerPort: 8080
        env:
        - name: PRODUCT_SERVICE_URL
          value: "http://product-service.ecommerce.svc.cluster.local:8080"
        - name: ORDER_SERVICE_URL
          value: "http://order-service.ecommerce.svc.cluster.local:8080"
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 200m
            memory: 256Mi
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: ecommerce
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: frontend
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: frontend-ingress
  namespace: ecommerce
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
      - path: /api/products
        pathType: Prefix
        backend:
          service:
            name: product-service
            port:
              number: 8080
      - path: /api/orders
        pathType: Prefix
        backend:
          service:
            name: order-service
            port:
              number: 8080
EOF

# Deploy to both clusters
kubectx east && kubectl apply -f frontend.yaml
kubectx west && kubectl apply -f frontend.yaml

echo "✓ Frontend deployed to both clusters"
```

# Step 8: Testing the Deployment

## Test East Cluster

```shell
echo "Testing East Cluster..."
kubectx east

# Get all pods
kubectl get pods -n ecommerce -o wide

# Test frontend
curl http://localhost:8080/

# Test product service
kubectl run curl-test --image=curlimages/curl -i --rm --restart=Never -n ecommerce -- \
  curl -s http://product-service:8080

# Test order service
kubectl run curl-test --image=curlimages/curl -i --rm --restart=Never -n ecommerce -- \
  curl -s http://order-service:8080

# Check endpoints
kubectl get endpoints -n ecommerce

echo "✓ East cluster tests completed"
```

## Test West Cluster

```shell
echo "Testing West Cluster..."
kubectx west

# Get all pods
kubectl get pods -n ecommerce -o wide

# Test frontend
curl http://localhost:9080/

# Test product service
kubectl run curl-test --image=curlimages/curl -i --rm --restart=Never -n ecommerce -- \
  curl -s http://product-service:8080

# Test order service
kubectl run curl-test --image=curlimages/curl -i --rm --restart=Never -n ecommerce -- \
  curl -s http://order-service:8080

echo "✓ West cluster tests completed"
```

# Step 9: Deploy Metrics Server for HPA

```shell
deploy_metrics_server() {
  local context=$1
  kubectx $context
  
  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
  
  # Patch for kind clusters
  kubectl patch deployment metrics-server -n kube-system --type='json' \
    -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'
  
  echo "Waiting for metrics-server in $context..."
  kubectl wait --for=condition=ready pod -l k8s-app=metrics-server -n kube-system --timeout=120s
  
  echo "✓ Metrics server deployed in $context"
}

deploy_metrics_server east
deploy_metrics_server west

# Wait a moment for metrics to be collected
sleep 30

# Verify metrics are available
kubectx east && kubectl top nodes && kubectl top pods -n ecommerce
kubectx west && kubectl top nodes && kubectl top pods -n ecommerce
```

# Step 10: Load Testing and Observing Scaling

```shell
# Install hey (HTTP load generator)
brew install hey

# Load test East cluster
echo "Starting load test on East cluster..."
hey -z 2m -c 50 -q 10 http://localhost:8080/ &

# Watch HPA in real-time
kubectx east
watch -n 2 'kubectl get hpa -n ecommerce && echo && kubectl get pods -n ecommerce | grep product-service'

# After 2 minutes, check scaling
kubectl get hpa product-service-hpa -n ecommerce
kubectl get pods -n ecommerce -l app=product-service

echo "✓ Load test completed - observe HPA scaling"
```

# Step 11: Simulate Failure Scenarios

## Scenario 1: Pod Failure

```shell
echo "=== Scenario 1: Simulating pod failure ==="
kubectx east

# Delete a pod
VICTIM_POD=$(kubectl get pods -n ecommerce -l app=product-service -o jsonpath='{.items[0].metadata.name}')
echo "Deleting pod: $VICTIM_POD"
kubectl delete pod $VICTIM_POD -n ecommerce

# Watch recovery
watch -n 1 'kubectl get pods -n ecommerce -l app=product-service'

echo "✓ Pod automatically recreated by ReplicaSet"
```

## Scenario 2: Node Failure (Drain)

```shell
echo "=== Scenario 2: Simulating node drain ==="
kubectx east

# Get a worker node
WORKER_NODE=$(kubectl get nodes -o jsonpath='{.items[?(@.metadata.name!="east-cluster-control-plane")].metadata.name}' | awk '{print $1}')

echo "Draining node: $WORKER_NODE"
kubectl drain $WORKER_NODE --ignore-daemonsets --delete-emptydir-data --force

# Watch pods rescheduling
kubectl get pods -n ecommerce -o wide

# Uncordon the node
kubectl uncordon $WORKER_NODE

echo "✓ Pods rescheduled to available nodes"
```

## Scenario 3: Service Unavailability

```shell
echo "=== Scenario 3: Scaling service to zero ==="
kubectx east

# Scale product service to 0
kubectl scale deployment product-service --replicas=0 -n ecommerce

# Try to access
kubectl run curl-test --image=curlimages/curl -i --rm --restart=Never -n ecommerce -- \
  curl -s --max-time 5 http://product-service:8080 || echo "Service unavailable as expected"

# Scale back up
kubectl scale deployment product-service --replicas=3 -n ecommerce

# Wait for pods
kubectl wait --for=condition=ready pod -l app=product-service -n ecommerce --timeout=60s

echo "✓ Service recovered"
```

# Step 12: Cross-Cluster Communication Test

```shell
# Get service IPs from both clusters
EAST_LB_IP=$(docker inspect east-cluster-control-plane | jq -r '.[0].NetworkSettings.Networks.kind.IPAddress')
WEST_LB_IP=$(docker inspect west-cluster-control-plane | jq -r '.[0].NetworkSettings.Networks.kind.IPAddress')

echo "East Cluster IP: $EAST_LB_IP"
echo "West Cluster IP: $WEST_LB_IP"

# Test cross-cluster connectivity (requires additional setup for production)
kubectx east
kubectl run cross-cluster-test --image=curlimages/curl -i --rm --restart=Never -n ecommerce -- \
  curl -s http://${WEST_LB_IP}:9080/ || echo "Cross-cluster requires additional networking setup"

echo "✓ Cross-cluster connectivity tested"
```

# Step 13: Observability with stern

```shell
# Install stern for multi-pod logging
brew install stern

# Watch logs from all product-service pods in east cluster
kubectx east
stern -n ecommerce product-service &

# Generate some traffic
for i in {1..20}; do
  kubectl run curl-test-$i --image=curlimages/curl --rm --restart=Never -n ecommerce -- \
    curl -s http://product-service:8080
done

# Stop stern
pkill stern

echo "✓ Observed logs from multiple pods simultaneously"
```

# Step 14: Backup and Restore

## Export Resources

```shell
# Export all resources from East cluster
kubectx east
kubectl get all -n ecommerce -o yaml > east-cluster-backup.yaml

# Export ConfigMaps and Secrets
kubectl get configmaps -n ecommerce -o yaml > east-configmaps-backup.yaml
kubectl get secrets -n ecommerce -o yaml > east-secrets-backup.yaml

echo "✓ Resources backed up"
```

## Disaster Recovery Simulation

```shell
# Delete everything in West cluster
kubectx west
kubectl delete namespace ecommerce

# Recreate namespace
kubectl create namespace ecommerce
kubectl label namespace ecommerce environment=production region=west managed-by=hands-on-lab

# Restore from East backup
kubectl apply -f east-cluster-backup.yaml
kubectl apply -f east-configmaps-backup.yaml

# Verify restoration
kubectl get all -n ecommerce

echo "✓ Disaster recovery completed"
```

# Step 15: Resource Usage Analysis

```shell
# Compare resource usage across clusters
echo "=== East Cluster Resources ==="
kubectx east
kubectl top nodes
kubectl top pods -n ecommerce --sort-by=cpu
echo

echo "=== West Cluster Resources ==="
kubectx west
kubectl top nodes
kubectl top pods -n ecommerce --sort-by=cpu
echo

# Get resource requests vs limits
echo "=== Resource Allocation ==="
kubectl get pods -n ecommerce -o json --context=east | \
  jq -r '.items[] | "\(.metadata.name): CPU req=\(.spec.containers[0].resources.requests.cpu) limit=\(.spec.containers[0].resources.limits.cpu) | MEM req=\(.spec.containers[0].resources.requests.memory) limit=\(.spec.containers[0].resources.limits.memory)"'
```

# Step 16: Network Policy Testing

```shell
cat > network-policy.yaml <<'EOF'
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
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
EOF

kubectx east
kubectl apply -f network-policy.yaml

# Test that only frontend can access product-service
echo "Testing network policy..."

# This should work (from frontend pod)
FRONTEND_POD=$(kubectl get pod -n ecommerce -l app=frontend -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $FRONTEND_POD -n ecommerce -- wget -qO- --timeout=2 http://product-service:8080

# This should fail (from random pod)
kubectl run unauthorized-test --image=curlimages/curl --rm -i --restart=Never -n ecommerce -- \
  curl -s --max-time 2 http://product-service:8080 || echo "✓ Network policy blocking unauthorized access"
```

# Summary and Cleanup

## What We Accomplished

1. ✓ Created multi-cluster environment (East & West)
2. ✓ Deployed distributed applications across clusters
3. ✓ Implemented StatefulSets for stateful services
4. ✓ Configured autoscaling with HPA
5. ✓ Set up ingress for external access
6. ✓ Tested failure scenarios and recovery
7. ✓ Implemented network policies
8. ✓ Practiced disaster recovery
9. ✓ Monitored resources and logs

## Cleanup

```shell
# Delete both clusters
kind delete cluster --name east-cluster
kind delete cluster --name west-cluster

# Remove backup files
rm -f east-cluster-backup.yaml east-configmaps-backup.yaml east-secrets-backup.yaml
rm -f redis-statefulset.yaml product-service.yaml order-service.yaml frontend.yaml network-policy.yaml

echo "✓ Cleanup completed"
```

# Next Steps

Now that you've completed this hands-on lab, try:

1. **Add monitoring** with Prometheus and Grafana
2. **Implement service mesh** with Istio or Linkerd
3. **Setup GitOps** with ArgoCD
4. **Add distributed tracing** with Jaeger
5. **Implement blue-green deployments**
6. **Setup cross-cluster service mesh**

# Key Takeaways

- **Multi-cluster** deployments provide high availability and disaster recovery
- **StatefulSets** maintain pod identity and persistent storage
- **HPA** automatically scales based on resource utilization
- **Network Policies** provide security isolation
- **Ingress** provides external access with routing rules
- **Affinity rules** control pod placement across nodes
- Kubernetes **self-heals** by recreating failed pods automatically

This hands-on experience gives you practical knowledge of running production-grade multi-cluster Kubernetes deployments!

