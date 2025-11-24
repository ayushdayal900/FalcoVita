#!/bin/bash

# Hospital Management System - Start All Services
# This script starts Redis, Celery Worker, Celery Beat, Flask Backend, and Vue Frontend

echo "🏥 Starting Hospital Management System..."

# Check if Redis is installed
if ! command -v redis-server &> /dev/null; then
    echo "❌ Redis is not installed. Please install Redis first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Virtual environment not found. Please run: cd backend && python -m venv venv"
    exit 1
fi

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Start Redis
echo -e "${BLUE}Starting Redis Server...${NC}"
redis-server --daemonize yes
sleep 2

# Activate virtual environment and start Celery Worker
echo -e "${BLUE}Starting Celery Worker...${NC}"
cd backend
source venv/bin/activate  # On Windows use: venv\Scripts\activate
celery -A backend.celery_config.celery_app worker --loglevel=info --detach
sleep 2

# Start Celery Beat
echo -e "${BLUE}Starting Celery Beat Scheduler...${NC}"
celery -A backend.celery_config.celery_app beat --loglevel=info --detach
sleep 2

# Start Flask Backend
echo -e "${BLUE}Starting Flask Backend...${NC}"
python app.py &
FLASK_PID=$!
cd ..
sleep 3

# Start Vue Frontend
echo -e "${BLUE}Starting Vue Frontend...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✅ All services started successfully!${NC}"
echo ""
echo "📍 Services running on:"
echo "   - Backend: http://127.0.0.1:5000"
echo "   - Frontend: http://localhost:5173"
echo "   - Redis: localhost:6379"
echo ""
echo "🛑 To stop all services, press Ctrl+C or run: ./stop_all.sh"
echo ""

# Wait for user to stop
wait