# System Prism - SRE Monitoring Stack Demonstration

A demonstration project showcasing the implementation of modern Site Reliability Engineering (SRE) monitoring methodologies and observability tools. This project evolved from a simple Flask application to a comprehensive Kubernetes-based monitoring stack, serving as a hands-on exploration of production-grade reliability engineering practices.

## Purpose

This is a personal learning project designed to demonstrate practical implementation of SRE concepts and modern observability tooling. Built to showcase:

- Integration of industry-standard monitoring and alerting tools
- Implementation of established SRE monitoring methodologies
- Evolution of architecture from monolithic to containerized deployment
- Operational practices including runbooks and actionable alerting

*Note: This is a portfolio demonstration and learning exercise rather than production-ready software intended for external deployment.*

## Architecture

- **Prometheus**: Time-series metrics collection and storage
- **Grafana**: Visualization dashboards and analytics
- **Loki**: Centralized log aggregation (via Promtail)
- **Alertmanager**: Intelligent alert routing and notification management
- **PostgreSQL**: Persistent data storage (evolved from SQLite)
- **Nginx**: Load balancing and reverse proxy
- **Kubernetes (Minikube)**: Container orchestration for scalability and resilience

## SRE Methodologies Demonstrated

### 1. USE Method Implementation (Infrastructure Monitoring)
**Utilization, Saturation, Errors**
- Tracks CPU/memory utilization and errors
- Saturation approximated via request processing time

### 2. RED Method Implementation (Service Monitoring)  
**Rate, Errors, Duration**
- Fully implemented with request rate, error counts, and latency metrics

### 3. Operational Excellence
- **Actionable Alerts**: Alerts implemented with runbooks
- **Runbook Integration**: Runbooks added with links to wiki
- **Dashboard Design**: Grafana dashboards covering metrics and logs

## Key Learning Outcomes

- Hands-on experience with the modern SRE observability stack
- Understanding of monitoring methodology implementation at scale
- Container orchestration for resilient monitoring infrastructure
- Operational practices for maintaining service reliability
