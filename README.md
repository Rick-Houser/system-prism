# System Prism

A comprehensive system for monitoring, logging, and alerting on application and infrastructure metrics, evolved from a Flask app to a Kubernetes-based deployment.

## Architecture

- **Prometheus**: Time-series metrics collection
- **Grafana**: Visualization and dashboards
- **Loki**: Log aggregation (via Promtail)
- **Alertmanager**: Alert routing and notification
- **PostgreSQL**: Persistent storage (replacing SQLite)
- **Nginx**: Load balancing across multiple instances
- **Kubernetes (Minikube)**: Orchestration for scalability and resilience

## Goals

1. **Implement the USE Method (Utilization, Saturation, Errors) for Infrastructure Monitoring**
   - Tracks CPU/memory utilization and errors; saturation approximated via request processing time.
2. **Implement the RED Method (Rate, Errors, Duration) for Service Monitoring**
   - Fully implemented with request rate, error counts, and latency metrics.
3. **Create Actionable Alerts with Runbooks**
   - Alerts implemented; runbooks added with links to wiki.
4. **Build Comprehensive Dashboards for Service Health**
   - Achieved with Grafana dashboards covering metrics and logs.