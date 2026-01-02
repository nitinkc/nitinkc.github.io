---
title: "Kubernetes Multi-Cluster Quick Reference"
date: 2025-04-30 08:00:00
categories:
- DevOps
tags:
- Kubernetes
- Cheat Sheet
- Quick Reference
---

{% include toc title="Index" %}

# Essential Multi-Cluster Commands

## Context Switching

| Command | Description |
|---------|-------------|
| `kubectx` | List all contexts |
| `kubectx east` | Switch to east cluster |
| `kubectx -` | Switch to previous context |
| `kubectx -c` | Show current context |
| `kubectl config get-contexts` | List contexts with details |
| `kubectl config current-context` | Show current context |

## Namespace Operations

| Command | Description |
|---------|-------------|
| `kubens` | List namespaces |
| `kubens ecommerce` | Switch to namespace |
| `kubens -` | Switch to previous namespace |
| `kubectl config set-context --current --namespace=ecommerce` | Set default namespace |

## Multi-Cluster Operations

```shell
# Apply to all clusters
for ctx in east west; do
  kubectl apply -f deployment.yaml --context=$ctx
done

# Get status from all clusters
for ctx in east west; do
  echo "=== $ctx ==="
  kubectl get pods -n ecommerce --context=$ctx
done

# Compare deployments
diff \
  <(kubectl get deploy -n ecommerce --context=east -o yaml) \
  <(kubectl get deploy -n ecommerce --context=west -o yaml)

# Scale across clusters
kubectl scale deployment product-service --replicas=5 -n ecommerce --context=east
kubectl scale deployment product-service --replicas=3 -n ecommerce --context=west
```

# Resource Management Quick Reference

## Pod Operations

| Command | Description |
|---------|-------------|
| `k get pods -n ecommerce` | List pods |
| `k get pods -o wide` | Show node and IP |
| `k describe pod <name>` | Detailed info |
| `k logs <pod>` | View logs |
| `k logs <pod> -f` | Follow logs |
| `k logs <pod> --previous` | Previous container logs |
| `k exec -it <pod> -- /bin/sh` | Shell into pod |
| `k delete pod <name>` | Delete pod |
| `k delete pod <name> --grace-period=0 --force` | Force delete |

## Deployment Operations

| Command | Description |
|---------|-------------|
| `k get deploy` | List deployments |
| `k describe deploy <name>` | Deployment details |
| `k scale deploy <name> --replicas=5` | Scale deployment |
| `k set image deploy/<name> container=image:tag` | Update image |
| `k rollout status deploy/<name>` | Check rollout status |
| `k rollout history deploy/<name>` | View rollout history |
| `k rollout undo deploy/<name>` | Rollback deployment |
| `k rollout restart deploy/<name>` | Restart all pods |

## Service Operations

| Command | Description |
|---------|-------------|
| `k get svc` | List services |
| `k describe svc <name>` | Service details |
| `k get endpoints <name>` | Show endpoints |
| `k port-forward svc/<name> 8080:80` | Port forward service |

# Debugging Commands

## Network Debugging

```shell
# DNS test
kubectl run dns-test --image=busybox:1.28 --rm -it --restart=Never -- nslookup kubernetes.default

# Connectivity test
kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never -- \
  curl -v http://product-service.ecommerce.svc.cluster.local:8080

# Network troubleshooting pod
kubectl run netshoot --image=nicolaka/netshoot --rm -it --restart=Never -- bash
```

## Resource Monitoring

```shell
# Top commands
kubectl top nodes
kubectl top pods -n ecommerce
kubectl top pods -n ecommerce --sort-by=cpu
kubectl top pods -n ecommerce --sort-by=memory

# Watch resources
watch -n 2 kubectl get pods -n ecommerce
kubectl get pods -n ecommerce -w

# Events
kubectl get events -n ecommerce --sort-by='.lastTimestamp'
kubectl get events -n ecommerce --field-selector type=Warning
```

## Log Aggregation

```shell
# Multiple pod logs with stern
stern -n ecommerce product-service
stern -n ecommerce product-service --since 5m
stern -n ecommerce "product-.*" --tail 50

# All logs from deployment
kubectl logs -n ecommerce -l app=product-service --all-containers=true

# Previous logs from all pods
kubectl logs -n ecommerce -l app=product-service --previous --all-containers=true
```

# JSONPath Queries

## Common Queries

```shell
# Get pod IPs
kubectl get pods -n ecommerce -o jsonpath='{.items[*].status.podIP}'

# Get pod names and nodes
kubectl get pods -n ecommerce -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.nodeName}{"\n"}{end}'

# Get all container images
kubectl get pods -n ecommerce -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u

# Get resource requests
kubectl get pods -n ecommerce -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].resources.requests}{"\n"}{end}'

# Get restart counts
kubectl get pods -n ecommerce -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[*].restartCount}{"\n"}{end}'
```

# Configuration Management

## ConfigMaps

```shell
# Create from literal
kubectl create configmap app-config --from-literal=key1=value1 --from-literal=key2=value2 -n ecommerce

# Create from file
kubectl create configmap app-config --from-file=config.yaml -n ecommerce

# View configmap
kubectl get configmap app-config -o yaml -n ecommerce

# Edit configmap
kubectl edit configmap app-config -n ecommerce

# Delete configmap
kubectl delete configmap app-config -n ecommerce
```

## Secrets

```shell
# Create generic secret
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=secret123 \
  -n ecommerce

# Create TLS secret
kubectl create secret tls tls-secret \
  --cert=path/to/cert.crt \
  --key=path/to/cert.key \
  -n ecommerce

# View secret (base64 encoded)
kubectl get secret db-secret -o yaml -n ecommerce

# Decode secret
kubectl get secret db-secret -o jsonpath='{.data.password}' -n ecommerce | base64 -d

# Delete secret
kubectl delete secret db-secret -n ecommerce
```

# Scaling and Performance

## Horizontal Pod Autoscaler

```shell
# Create HPA
kubectl autoscale deployment product-service \
  --cpu-percent=70 \
  --min=3 \
  --max=10 \
  -n ecommerce

# Get HPA status
kubectl get hpa -n ecommerce

# Watch HPA
kubectl get hpa -n ecommerce -w

# Describe HPA
kubectl describe hpa product-service-hpa -n ecommerce

# Delete HPA
kubectl delete hpa product-service-hpa -n ecommerce
```

## Resource Management

```shell
# Set resource limits
kubectl set resources deployment product-service \
  --requests=cpu=200m,memory=256Mi \
  --limits=cpu=1000m,memory=512Mi \
  -n ecommerce

# Check resource usage
kubectl describe nodes | grep -A 5 "Allocated resources"

# Get pod QoS class
kubectl get pods -n ecommerce -o custom-columns=NAME:.metadata.name,QOS:.status.qosClass
```

# Troubleshooting Scenarios

## Pod Stuck in Pending

```shell
# Check events
kubectl describe pod <pod-name> -n ecommerce | grep -A 10 Events

# Check node resources
kubectl describe nodes

# Check PVC status
kubectl get pvc -n ecommerce

# Check node selector/affinity
kubectl get pod <pod-name> -n ecommerce -o yaml | grep -A 10 nodeSelector
```

## Pod CrashLoopBackOff

```shell
# Check logs
kubectl logs <pod-name> -n ecommerce --previous

# Check liveness/readiness probes
kubectl describe pod <pod-name> -n ecommerce | grep -A 5 "Liveness\|Readiness"

# Check events
kubectl get events -n ecommerce --field-selector involvedObject.name=<pod-name>

# Describe pod
kubectl describe pod <pod-name> -n ecommerce
```

## Service Not Accessible

```shell
# Check service
kubectl get svc <service-name> -n ecommerce
kubectl describe svc <service-name> -n ecommerce

# Check endpoints
kubectl get endpoints <service-name> -n ecommerce

# Verify pod labels match service selector
kubectl get pods -n ecommerce --show-labels
kubectl describe svc <service-name> -n ecommerce | grep Selector

# Test from within cluster
kubectl run test --image=curlimages/curl -it --rm --restart=Never -n ecommerce -- \
  curl -v http://<service-name>.<namespace>.svc.cluster.local:<port>
```

## Node Issues

```shell
# Check node status
kubectl get nodes
kubectl describe node <node-name>

# Check node conditions
kubectl get nodes -o json | jq '.items[] | {name:.metadata.name, conditions:.status.conditions}'

# Drain node
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Uncordon node
kubectl uncordon <node-name>

# Mark node unschedulable
kubectl cordon <node-name>
```

# Security Commands

## RBAC

```shell
# Check permissions
kubectl auth can-i create deployments -n ecommerce
kubectl auth can-i delete pods --all-namespaces

# Check as service account
kubectl auth can-i get pods \
  --as=system:serviceaccount:ecommerce:product-service-sa \
  -n ecommerce

# List permissions
kubectl auth can-i --list -n ecommerce
```

## Network Policies

```shell
# List network policies
kubectl get networkpolicy -n ecommerce

# Describe policy
kubectl describe networkpolicy <policy-name> -n ecommerce

# Test connectivity
kubectl run test-$RANDOM --image=busybox --rm -it --restart=Never -n ecommerce -- \
  wget --spider --timeout=1 http://product-service:8080
```

# Batch Operations

```shell
# Delete all pods with status
kubectl delete pods --field-selector status.phase=Failed -n ecommerce
kubectl delete pods --field-selector status.phase=Succeeded -n ecommerce

# Restart all deployments
kubectl rollout restart deployment --all -n ecommerce

# Label all pods
kubectl label pods --all environment=production -n ecommerce

# Get all resource types
kubectl get all -n ecommerce

# Delete all resources
kubectl delete all --all -n ecommerce

# Export all resources
kubectl get all -n ecommerce -o yaml > backup.yaml
```

# Useful Aliases

Add to `~/.zshrc`:

```shell
# Kubectl aliases
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kgd='kubectl get deployments'
alias kga='kubectl get all'
alias kgn='kubectl get nodes'

# Describe aliases
alias kdp='kubectl describe pod'
alias kds='kubectl describe service'
alias kdd='kubectl describe deployment'

# Logs aliases
alias kl='kubectl logs'
alias klf='kubectl logs -f'
alias klp='kubectl logs --previous'

# Execute aliases
alias kex='kubectl exec -it'

# Delete aliases
alias kdel='kubectl delete'
alias kdelp='kubectl delete pod'

# Context aliases
alias kctx='kubectl config use-context'
alias kcurrent='kubectl config current-context'
alias kns='kubectl config set-context --current --namespace'

# Watch aliases
alias kwatch='watch -n 2 kubectl get pods'
alias kwatchd='watch -n 2 kubectl get deployments'

# Multi-cluster aliases
alias keast='kubectl config use-context east'
alias kwest='kubectl config use-context west'

# Apply source
source ~/.zshrc
```

# Quick Diagnostic Script

```shell
#!/bin/bash
# Save as k8s-diagnostic.sh

NAMESPACE=${1:-ecommerce}
CONTEXT=${2:-$(kubectl config current-context)}

echo "=== Kubernetes Diagnostic Report ==="
echo "Context: $CONTEXT"
echo "Namespace: $NAMESPACE"
echo "Time: $(date)"
echo

echo "=== Nodes ==="
kubectl get nodes --context=$CONTEXT
echo

echo "=== Pods ==="
kubectl get pods -n $NAMESPACE --context=$CONTEXT -o wide
echo

echo "=== Services ==="
kubectl get svc -n $NAMESPACE --context=$CONTEXT
echo

echo "=== Deployments ==="
kubectl get deployments -n $NAMESPACE --context=$CONTEXT
echo

echo "=== HPA ==="
kubectl get hpa -n $NAMESPACE --context=$CONTEXT 2>/dev/null || echo "No HPA found"
echo

echo "=== Recent Events ==="
kubectl get events -n $NAMESPACE --context=$CONTEXT --sort-by='.lastTimestamp' | tail -10
echo

echo "=== Resource Usage ==="
kubectl top nodes --context=$CONTEXT 2>/dev/null || echo "Metrics server not available"
kubectl top pods -n $NAMESPACE --context=$CONTEXT 2>/dev/null || echo "Metrics server not available"
```

Usage:
```shell
chmod +x k8s-diagnostic.sh
./k8s-diagnostic.sh ecommerce east
./k8s-diagnostic.sh ecommerce west
```

# Performance Tuning Tips

## Pod Optimization

- Always set resource requests and limits
- Use readiness probes to prevent premature traffic
- Use liveness probes for automatic restart
- Configure appropriate termination grace period
- Use init containers for setup tasks

## Deployment Strategies

```shell
# Rolling update with max surge/unavailable
kubectl patch deployment product-service -p '{
  "spec": {
    "strategy": {
      "type": "RollingUpdate",
      "rollingUpdate": {
        "maxSurge": 1,
        "maxUnavailable": 0
      }
    }
  }
}' -n ecommerce

# Blue-green: switch service selector
kubectl patch service product-service -p '{
  "spec": {
    "selector": {
      "version": "v2"
    }
  }
}' -n ecommerce
```

## Resource Quotas

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ecommerce-quota
  namespace: ecommerce
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    persistentvolumeclaims: "10"
    pods: "50"
```

# Monitoring Checklist

- [ ] Metrics server installed
- [ ] Resource requests/limits set
- [ ] HPA configured for critical services
- [ ] Liveness and readiness probes configured
- [ ] Network policies in place
- [ ] Resource quotas defined
- [ ] Pod disruption budgets set
- [ ] Logging solution deployed
- [ ] Monitoring dashboards created
- [ ] Alerts configured

# Common Issues and Solutions

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| ImagePullBackOff | Check image name and registry access | Verify image exists, check secrets |
| CrashLoopBackOff | Check application logs | Fix application errors, check probes |
| Pending pods | Check node resources and taints | Scale cluster or adjust requests |
| Service unreachable | Check endpoints and selectors | Fix label matching |
| High latency | Check resource usage | Scale up or optimize app |
| OOMKilled | Check memory limits | Increase limits or fix memory leaks |

# Best Practices Summary

1. **Always use namespaces** for resource isolation
2. **Set resource requests and limits** for predictable performance
3. **Use labels and selectors** consistently
4. **Implement health checks** (liveness and readiness)
5. **Use ConfigMaps and Secrets** for configuration
6. **Enable autoscaling** (HPA) for dynamic workloads
7. **Implement network policies** for security
8. **Use StatefulSets** for stateful applications
9. **Regular backups** of cluster configuration
10. **Monitor everything** - resources, logs, metrics

This quick reference provides essential commands and patterns for managing multi-cluster Kubernetes deployments!

