# FastAPI with Kubernetes, Prometheus, and Grafana Monitoring Tutorial

A comprehensive 6-step guide to deploying FastAPI applications on Kubernetes with robust monitoring using Prometheus and Grafana.

## Overview

This tutorial covers deploying a FastAPI application to Kubernetes with complete monitoring setup. You'll learn:

- Setting up Kubernetes deployments for FastAPI applications
- Configuring service discovery and monitoring with Prometheus
- Creating Grafana dashboards for metric visualization
- Troubleshooting common deployment issues

## Step 1: Deploy FastAPI on Kubernetes

### Implementation Steps
- Containerize FastAPI using uv package manager
- Create and apply Kubernetes Deployment and Service
- Configure proper labels and selectors

### FastAPI Deployment Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
        - name: fastapi
          image: cshorten/fastapi-app:latest
          ports:
            - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
  labels:
    app: fastapi
spec:
  selector:
    app: fastapi
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8000
```

## Step 2: Install Prometheus for Monitoring

### Implementation Steps
- Install Prometheus Operator using Helm
- Verify StatefulSet deployment
- Check service discovery in Prometheus UI

### Installation Commands

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

## Step 3: Configure Prometheus Service Discovery

### ServiceMonitor Configuration

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: fastapi-servicemonitor
  namespace: monitoring
  labels:
    release: prometheus-stack
spec:
  selector:
    matchLabels:
      app: fastapi
  endpoints:
    - port: http
      path: /metrics
  namespaceSelector:
    matchNames:
      - default
```

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Missing FastAPI in targets | Verify ServiceMonitor configuration |
| FastAPI status DOWN | Check ServiceMonitor namespace selection |
| No active targets | Ensure service port is named 'http' |

## Step 4: Verify Prometheus Configuration

### Debugging Commands

```bash
# Port forward Prometheus service
kubectl port-forward -n monitoring svc/prometheus-stack-kube-prom-prometheus 9090

# Check Prometheus logs
kubectl logs -l app.kubernetes.io/name=prometheus -n monitoring --tail=50

# List ServiceMonitors
kubectl get servicemonitor -n monitoring

# Show pod labels
kubectl get pods -n monitoring --show-labels

# Restart Prometheus
kubectl rollout restart statefulset prometheus-prometheus-stack-kube-prom-prometheus -n monitoring
```

## Step 5: Grafana Dashboard Setup

### Access Configuration

```bash
# Port forward Grafana service
kubectl port-forward -n monitoring svc/prometheus-stack-grafana 3000

# Get admin password
kubectl get secret -n monitoring prometheus-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

### Prometheus Data Source Configuration
1. Navigate to Configuration → Data Sources
2. Select Prometheus
3. Set URL to: `http://prometheus-stack-kube-prom-prometheus.monitoring.svc:9090`
4. Save and test connection

## Step 6: Metric Visualization

### Essential PromQL Queries

| Query | Description |
|-------|-------------|
| `request_count_total` | Total number of FastAPI requests |
| `rate(request_count_total[5m])` | Request rate per second (5m window) |
| `avg_over_time(request_count_total[1h])` | Average hourly requests |

## Next Steps

### Enhancement Opportunities
1. **Metric Expansion**
   - Implement Histogram and Summary metrics
   - Add custom business metrics

2. **Alert Configuration**
   - Set up Prometheus AlertManager
   - Configure alert rules and notifications

3. **Scaling Implementation**
   - Configure HorizontalPodAutoscaler
   - Define scaling metrics and thresholds

## Achievement Checklist

- [x] FastAPI deployment on Kubernetes
- [x] Prometheus metric collection
- [x] Grafana dashboard visualization
- [x] Service discovery configuration
- [x] Basic monitoring setup
