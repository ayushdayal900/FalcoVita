#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "===================================================="
echo "          Starting FalcoVita Services               "
echo "===================================================="

# Check if .env file exists in root
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "Please verify and update the .env file with your specific environment configurations."
fi

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker daemon is not running. Please start Docker Desktop/Daemon and try again."
    exit 1
fi

echo "🚀 Building and starting containers..."
docker-compose up --build -d

echo "===================================================="
echo "🎉 All services started successfully!"
echo "===================================================="
echo "You can access the services at the following URLs:"
echo "----------------------------------------------------"
echo "🖥️  Frontend:        http://localhost:3000"
echo "⚙️  Backend API:      http://localhost:5000"
echo "🌐 GraphQL Play:     http://localhost:5000/graphql"
echo "📈 Prometheus:       http://localhost:9090"
echo "📊 Grafana:          http://localhost:3001  (User: admin, Pass: admin)"
echo "🔍 OpenSearch:       http://localhost:9200"
echo "📧 Mailhog Web UI:   http://localhost:8026"
echo "===================================================="
