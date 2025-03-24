#!/usr/bin/env bash
set -e

# Build and start services
docker-compose up -d

# Wait for services to start
sleep 5

# Test GET /tasks
response=$(curl -s http://localhost:5000/tasks)
if [ "$response" = "[]" ]; then
    echo "GET /tasks test passed"
else
    echo "GET /tasks test failed: expected [], got $response"
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
if [ "$prom_status" = "Prometheus is Healthy." ]; then
    echo "Prometheus health check passed"
else
    echo "Prometheus health check failed"
    exit 1
fi

# Test Grafana
grafana_status=$(curl -s http://localhost:3000/api/health | grep -o '"database":"ok"')
if [ "$grafana_status" = '"database":"ok"' ]; then
    echo "Grafana health check passed"
else
    echo "Grafana health check failed"
    exit 1
fi

# Clean up
docker-compose down

echo "Container tests passed!"