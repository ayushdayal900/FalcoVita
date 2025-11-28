#!/bin/bash

# Hospital Management System - Stop All Services

echo "🛑 Stopping Hospital Management System services..."

# Stop Flask (if running)
pkill -f "python app.py"

# Stop Celery Worker
pkill -f "celery.*worker"

# Stop Celery Beat
pkill -f "celery.*beat"

# Stop Redis
redis-cli shutdown

# Stop Vue dev server
pkill -f "npm run dev"
pkill -f "vite"

echo "✅ All services stopped."