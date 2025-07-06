#!/bin/bash

# Development startup script

echo "Starting Neural Machine Translation System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is required but not installed."
    exit 1
fi

echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt

echo "Starting backend server..."
python -m app.main &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 5

echo "Installing frontend dependencies..."
cd ../frontend
npm install

echo "Starting frontend server..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🚀 Neural Machine Translation System is starting..."
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup processes
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for processes
wait
