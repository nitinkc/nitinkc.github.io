---
title: "Advanced Kubernetes Patterns: Service Mesh, Security & GitOps"
date: 2025-04-30 06:00:00
categories:
- DevOps
tags:
- Kubernetes
- Istio
- GitOps
- Security
- ArgoCD
---

{% include toc title="Index" %}

# Advanced Kubernetes Patterns

This guide covers production-grade patterns including service mesh with Istio, advanced security configurations, GitOps with ArgoCD, and comprehensive observability.

# Service Mesh with Istio

## Installation

```shell
# Download Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

# Install Istio with demo profile
istioctl install --set profile=demo -y

# Verify installation
kubectl get pods -n istio-system

# Enable sidecar injection for namespace
kubectl label namespace ecommerce istio-injection=enabled
```

## Traffic Management Patterns

### 1. Canary Deployment with Traffic Splitting

`istio/canary-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service-v2
  namespace: ecommerce
spec:
  replicas: 2
  selector:
    matchLabels:
      app: product-service
      version: v2
  template:
    metadata:
      labels:
        app: product-service
        version: v2
    spec:
      containers:
      - name: product-service
        image: nitinkc/product-service:v2.0
        ports:
        - containerPort: 8080
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: product-service
  namespace: ecommerce
spec:
  hosts:
  - product-service
  http:
  - match:
    - headers:
        user-agent:
          regex: ".*Chrome.*"
    route:
    - destination:
        host: product-service
        subset: v2
      weight: 100
  - route:
    - destination:
        host: product-service
        subset: v1
      weight: 90
    - destination:
        host: product-service
        subset: v2
      weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: product-service
  namespace: ecommerce
spec:
  host: product-service
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

### 2. A/B Testing with Header-Based Routing

`istio/ab-testing.yaml`
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ab-test-frontend
  namespace: ecommerce
spec:
  hosts:
  - frontend.ecommerce.svc.cluster.local
  http:
  - match:
    - headers:
        x-user-type:
          exact: "premium"
    route:
    - destination:
        host: frontend
        subset: premium
  - match:
    - headers:
        cookie:
          regex: "^(.*?;)?(experiment=variant-b)(;.*)?$"
    route:
    - destination:
        host: frontend
        subset: variant-b
  - route:
    - destination:
        host: frontend
        subset: stable
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: frontend-subsets
  namespace: ecommerce
spec:
  host: frontend
  subsets:
  - name: stable
    labels:
      version: stable
  - name: variant-b
    labels:
      version: variant-b
  - name: premium
    labels:
      version: premium
```

### 3. Circuit Breaker and Retry Logic

`istio/resilience.yaml`
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: order-service-resilience
  namespace: ecommerce
spec:
  host: order-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutiveGatewayErrors: 5
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 40
    loadBalancer:
      simple: LEAST_REQUEST
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: order-service-retry
  namespace: ecommerce
spec:
  hosts:
  - order-service
  http:
  - retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: 5xx,reset,connect-failure,refused-stream
    timeout: 10s
    route:
    - destination:
        host: order-service
```

### 4. Rate Limiting

`istio/rate-limit.yaml`
```yaml
apiVersion: networking.istio.io/v1beta1
kind: EnvoyFilter
metadata:
  name: filter-ratelimit
  namespace: istio-system
spec:
  workloadSelector:
    labels:
      app: istio-ingressgateway
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: GATEWAY
      listener:
        filterChain:
          filter:
            name: "envoy.filters.network.http_connection_manager"
            subFilter:
              name: "envoy.filters.http.router"
    patch:
      operation: INSERT_BEFORE
      value:
        name: envoy.filters.http.local_ratelimit
        typed_config:
          "@type": type.googleapis.com/udpa.type.v1.TypedStruct
          type_url: type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
          value:
            stat_prefix: http_local_rate_limiter
            token_bucket:
              max_tokens: 100
              tokens_per_fill: 100
              fill_interval: 60s
            filter_enabled:
              runtime_key: local_rate_limit_enabled
              default_value:
                numerator: 100
                denominator: HUNDRED
            filter_enforced:
              runtime_key: local_rate_limit_enforced
              default_value:
                numerator: 100
                denominator: HUNDRED
```

## Deploy and Test Traffic Management

```shell
# Apply Istio configurations
kubectl apply -f istio/

# Test canary deployment
for i in {1..100}; do
  curl -s http://product-service.ecommerce.svc.cluster.local:8080/version | grep version
done | sort | uniq -c

# Test with different headers
curl -H "user-agent: Chrome/90.0" http://product-service/api/products

# Observe traffic in Kiali
istioctl dashboard kiali
```

# Advanced Security Patterns

## 1. mTLS Between Services

```shell
# Enable strict mTLS for entire namespace
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: ecommerce
spec:
  mtls:
    mode: STRICT
EOF

# Verify mTLS
kubectl exec -it <pod-name> -c istio-proxy -n ecommerce -- \
  curl http://localhost:15000/config_dump | grep -A 10 tls_context
```

## 2. Authorization Policies

`security/authorization-policies.yaml`
```yaml
# Allow only frontend to call product service
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: product-service-authz
  namespace: ecommerce
spec:
  selector:
    matchLabels:
      app: product-service
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/ecommerce/sa/frontend"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/api/products*"]
---
# Deny all DELETE operations
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-delete
  namespace: ecommerce
spec:
  action: DENY
  rules:
  - to:
    - operation:
        methods: ["DELETE"]
---
# Allow only specific IP ranges
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: ip-allowlist
  namespace: ecommerce
spec:
  selector:
    matchLabels:
      app: order-service
  action: ALLOW
  rules:
  - from:
    - source:
        ipBlocks: ["10.0.0.0/8", "172.16.0.0/12"]
    when:
    - key: request.headers[x-api-key]
      values: ["secret-api-key-123"]
```

## 3. JWT Authentication

`security/jwt-auth.yaml`
```yaml
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: jwt-auth
  namespace: ecommerce
spec:
  selector:
    matchLabels:
      app: frontend
  jwtRules:
  - issuer: "https://auth.example.com"
    jwksUri: "https://auth.example.com/.well-known/jwks.json"
    audiences:
    - "ecommerce-api"
    forwardOriginalToken: true
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
  namespace: ecommerce
spec:
  selector:
    matchLabels:
      app: frontend
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["*"]
    when:
    - key: request.auth.claims[role]
      values: ["user", "admin"]
```

## 4. Pod Security Standards

`security/pod-security.yaml`
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-product-service
  namespace: ecommerce
spec:
  replicas: 3
  selector:
    matchLabels:
      app: product-service
  template:
    metadata:
      labels:
        app: product-service
    spec:
      serviceAccountName: product-service-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: product-service
        image: nitinkc/product-service:v1.0
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
```

## 5. Service Accounts with RBAC

`security/rbac.yaml`
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: product-service-sa
  namespace: ecommerce
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: product-service-role
  namespace: ecommerce
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["product-service-secret"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: product-service-binding
  namespace: ecommerce
subjects:
- kind: ServiceAccount
  name: product-service-sa
  namespace: ecommerce
roleRef:
  kind: Role
  name: product-service-role
  apiGroup: rbac.authorization.k8s.io
```

Apply security configurations:
```shell
kubectl apply -f security/
```

# GitOps with ArgoCD

## Install ArgoCD

```shell
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## ArgoCD Application Definition

`argocd/ecommerce-app.yaml`
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ecommerce-east
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/nitinkc/k8s-manifests.git'
    targetRevision: HEAD
    path: ecommerce/overlays/east
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: ecommerce
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ecommerce-west
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/nitinkc/k8s-manifests.git'
    targetRevision: HEAD
    path: ecommerce/overlays/west
  destination:
    server: 'https://west-cluster-api.example.com'
    namespace: ecommerce
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Kustomize Structure for Multi-Environment

```
k8s-manifests/
├── ecommerce/
│   ├── base/
│   │   ├── kustomization.yaml
│   │   ├── product-service/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── order-service/
│   │   │   ├── statefulset.yaml
│   │   │   └── service.yaml
│   │   └── frontend/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       └── ingress.yaml
│   └── overlays/
│       ├── east/
│       │   ├── kustomization.yaml
│       │   ├── replica-patch.yaml
│       │   └── config-patch.yaml
│       └── west/
│           ├── kustomization.yaml
│           ├── replica-patch.yaml
│           └── config-patch.yaml
```

`base/kustomization.yaml`
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- product-service/deployment.yaml
- product-service/service.yaml
- order-service/statefulset.yaml
- order-service/service.yaml
- frontend/deployment.yaml
- frontend/service.yaml
- frontend/ingress.yaml

commonLabels:
  app.kubernetes.io/managed-by: kustomize
  app.kubernetes.io/part-of: ecommerce
```

`overlays/east/kustomization.yaml`
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: ecommerce

bases:
- ../../base

commonLabels:
  environment: production
  region: us-east-1

patches:
- path: replica-patch.yaml
- path: config-patch.yaml

configMapGenerator:
- name: region-config
  literals:
  - REGION=us-east-1
  - PRIMARY=true
  - PEER_ENDPOINT=https://west.example.com

secretGenerator:
- name: db-credentials
  literals:
  - DB_HOST=east-db.example.com
  - DB_PORT=5432
```

`overlays/east/replica-patch.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service
spec:
  replicas: 5
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 4
```

Deploy with ArgoCD:
```shell
kubectl apply -f argocd/ecommerce-app.yaml

# Watch sync status
argocd app list
argocd app get ecommerce-east
argocd app sync ecommerce-east
```

# Observability Stack

## 1. Distributed Tracing with Jaeger

```shell
# Install Jaeger
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml

# Access Jaeger UI
istioctl dashboard jaeger

# Generate traces
kubectl exec -it <frontend-pod> -n ecommerce -- \
  curl -H "x-b3-sampled: 1" http://product-service:8080/api/products
```

## 2. Metrics with Prometheus and Grafana

`monitoring/servicemonitor.yaml`
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: product-service-monitor
  namespace: ecommerce
  labels:
    app: product-service
spec:
  selector:
    matchLabels:
      app: product-service
  endpoints:
  - port: http
    path: /actuator/prometheus
    interval: 30s
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: product-service-alerts
  namespace: ecommerce
spec:
  groups:
  - name: product-service
    interval: 30s
    rules:
    - alert: HighErrorRate
      expr: |
        rate(http_server_requests_seconds_count{status=~"5..",job="product-service"}[5m]) > 0.05
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High error rate on product service"
        description: "Error rate is {{ $value }} requests/sec"
    - alert: HighLatency
      expr: |
        histogram_quantile(0.95, rate(http_server_requests_seconds_bucket{job="product-service"}[5m])) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High latency on product service"
        description: "95th percentile latency is {% raw %}{{ $value }}{% endraw %}s"
```

## 3. Logging with EFK Stack

`logging/fluentd-config.yaml`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>

    <filter kubernetes.**>
      @type kubernetes_metadata
      @id filter_kube_metadata
    </filter>

    <filter kubernetes.**>
      @type record_transformer
      <record>
        cluster_name "#{ENV['CLUSTER_NAME']}"
        region "#{ENV['REGION']}"
      </record>
    </filter>

    <match kubernetes.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      logstash_format true
      logstash_prefix kubernetes-${record['kubernetes']['namespace_name']}
      <buffer>
        @type file
        path /var/log/fluentd-buffers/kubernetes.system.buffer
        flush_mode interval
        retry_type exponential_backoff
        flush_interval 5s
        retry_forever
        retry_max_interval 30
        chunk_limit_size 2M
        queue_limit_length 8
        overflow_action block
      </buffer>
    </match>
```

# Advanced Deployment Strategies

## Blue-Green Deployment

`deployments/blue-green.yaml`
```yaml
# Blue deployment (current stable)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-blue
  namespace: ecommerce
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
      version: blue
  template:
    metadata:
      labels:
        app: frontend
        version: blue
    spec:
      containers:
      - name: frontend
        image: nitinkc/frontend:v1.0
---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-green
  namespace: ecommerce
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
      version: green
  template:
    metadata:
      labels:
        app: frontend
        version: green
    spec:
      containers:
      - name: frontend
        image: nitinkc/frontend:v2.0
---
# Service pointing to blue initially
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: ecommerce
spec:
  selector:
    app: frontend
    version: blue
  ports:
  - port: 80
    targetPort: 3000
```

Switch traffic:
```shell
# Test green deployment
kubectl port-forward svc/frontend-green 8080:80 -n ecommerce

# Switch traffic to green
kubectl patch service frontend -n ecommerce -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback if needed
kubectl patch service frontend -n ecommerce -p '{"spec":{"selector":{"version":"blue"}}}'

# Delete old blue deployment
kubectl delete deployment frontend-blue -n ecommerce
```

# Chaos Engineering

`chaos/pod-kill.yaml`
```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: kill-product-service
  namespace: ecommerce
spec:
  action: pod-kill
  mode: one
  duration: "30s"
  selector:
    namespaces:
    - ecommerce
    labelSelectors:
      app: product-service
  scheduler:
    cron: "*/5 * * * *"
```

# Complete Monitoring Dashboard Query Examples

## Prometheus Queries

```promql
# Request rate
rate(http_server_requests_seconds_count[5m])

# Error rate
rate(http_server_requests_seconds_count{status=~"5.."}[5m])

# P95 latency
histogram_quantile(0.95, rate(http_server_requests_seconds_bucket[5m]))

# Pod CPU usage
rate(container_cpu_usage_seconds_total{namespace="ecommerce"}[5m])

# Pod memory usage
container_memory_usage_bytes{namespace="ecommerce"}

# Network traffic
rate(container_network_receive_bytes_total{namespace="ecommerce"}[5m])
```

# Summary

This guide covered:
- **Service Mesh**: Traffic management, canary deployments, A/B testing
- **Security**: mTLS, authorization policies, JWT auth, RBAC, pod security
- **GitOps**: ArgoCD for declarative deployments across clusters
- **Observability**: Distributed tracing, metrics, logging
- **Advanced Deployments**: Blue-green, canary with progressive delivery
- **Chaos Engineering**: Testing resilience with chaos experiments

These patterns enable production-ready, secure, and observable multi-cluster Kubernetes deployments.

