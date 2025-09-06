#!/bin/bash

# Project Nova - Bash Startup Script (Linux/Mac)
# This script starts both backend and frontend automatically

echo ""
echo "================================================================"
echo "🚀 PROJECT NOVA - EQUITABLE CREDIT SCORING ENGINE"
echo "================================================================"
echo "Starting automated setup..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Use python3 if available, otherwise python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

echo "✅ Python found: $($PYTHON_CMD --version)"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+ first."
    exit 1
fi

echo "✅ Node.js found: $(node --version)"
echo ""

# Navigate to project directory
PROJECT_PATH="$HOME/project-nova"  # Adjust this path as needed
cd "$PROJECT_PATH" || {
    echo "❌ Cannot navigate to project directory: $PROJECT_PATH"
    echo "Please update the PROJECT_PATH variable in this script to match your setup."
    exit 1
}

# Verify we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Cannot find backend/main.py. Please check if you're in the correct directory."
    exit 1
fi

if [ ! -f "frontend/package.json" ]; then
    echo "❌ Cannot find frontend/package.json. Please check if you're in the correct directory."
    exit 1
fi

echo "🔧 Setting up backend environment..."
cd backend

# Install Python dependencies
echo "Installing Python packages..."
$PIP_CMD install fastapi==0.104.1 uvicorn==0.24.0 pandas==2.1.3 scikit-learn==1.3.2 pydantic==2.5.0 python-multipart==0.0.6 joblib==1.3.2 requests==2.31.0 > /dev/null 2>&1

# Check if model exists, if not train it
if [ ! -f "credit_model.pkl" ]; then
    echo "🧠 Training ML model..."
    $PYTHON_CMD train_model.py
else
    echo "✅ ML model already exists"
fi

echo ""
echo "🎨 Setting up frontend environment..."
cd ../frontend

# Install Node.js dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js packages..."
    npm install > /dev/null 2>&1
else
    echo "✅ Node.js packages already installed"
fi

echo ""
echo "🚀 Starting Project Nova..."
echo ""
echo "Backend will start on: http://localhost:8000"
echo "Frontend will start on: http://localhost:3000"
echo ""
read -p "Press Enter to continue..."

# Start backend in background
echo "Starting backend server..."
cd ../backend
$PYTHON_CMD main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "================================================================"
echo "🎉 PROJECT NOVA IS RUNNING!"
echo "================================================================"
echo ""
echo "Backend: http://localhost:8000 (PID: $BACKEND_PID)"
echo "Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "To stop the servers, press Ctrl+C or run:"
echo "kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Keep script running
wait
