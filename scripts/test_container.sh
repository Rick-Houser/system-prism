#!/bin/bash
set -e

# Build the image
docker build -t flask-app:test .

# Run the container in the background
docker run -d -p 5000:5000 --name flask-app-test flask-app:test

# Wait briefly for the app to start
sleep 2

# Test GET /tasks
response=$(curl -s http://localhost:5000/tasks)
if [ "$response" = "[]" ]; then
    echo "GET /tasks test passed"
else
    echo "GET /tasks test failed: expected [], got $response"
    exit 1
fi

# Clean up
docker stop flask-app-test
docker rm flask-app-test

echo "Container tests passed!"