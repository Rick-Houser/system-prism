#!/usr/bin/env bash
set -e

# Build and start services
docker-compose up -d

# Wait for services to start
sleep 10

# Test CRUD - POST
curl -s -X POST -H "Content-Type: application/json" -d '{"task": "Test task"}' http://localhost:5000/tasks
response=$(curl -s http://localhost:5000/tasks)
if echo "$response" | grep -q "Test task"; then
    echo "CRUD - POST test passed"
else
    echo "CRUD - POST test failed, got $response"
    exit 1
fi

# Test metrics endpoint
metrics=$(curl -s http://localhost:8000)
if echo "$metrics" | grep -q "request_count"; then
    echo "Metrics endpoint test passed"
else
    echo "Metrics endpoint test failed: no request_count found"
    exit 1
fi

# Test Prometheus
prom_status=$(curl -s http://localhost:9090/-/healthy)
if echo "$prom_status" | grep -q "Prometheus is Healthy"; then
    echo "Prometheus health check passed"
else
    echo "Prometheus health check failed"
    exit 1
fi

# Test Grafana
grafana_status=$(curl -s http://localhost:3000/api/health)
if echo "$grafana_status" | grep -q '"database": "ok"'; then
    echo "Grafana health check passed"
else
    echo "Grafana health check failed"
    exit 1
fi

# Test Alertmanager
alertmanager_status=$(curl -s http://localhost:9093/-/healthy)
if echo "$alertmanager_status" | grep -q "OK"; then
    echo "Alertmanager health check passed"
else
    echo "Alertmanager health check failed"
    exit 1
fi

# Test Loki
loki_status=$(curl -s http://localhost:3100/ready)
if echo "$loki_status" | grep -q "ready"; then
    echo "Loki test passed"
else
    echo "Loki test failed"
    exit 1
fi

# Clean up
docker-compose down

echo "Container tests passed!"