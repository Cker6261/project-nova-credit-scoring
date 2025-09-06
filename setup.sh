#!/bin/bash

# Project Nova Setup Script
# This script sets up the entire project for development

echo "🚀 Setting up Project Nova - Equitable Credit Scoring Engine"
echo "============================================================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Backend
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
python -m venv nova_env
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source nova_env/Scripts/activate
else
    source nova_env/bin/activate
fi

# Install Python dependencies
pip install -r requirements.txt

# Train the ML model
echo "🧠 Training ML model..."
python train_model.py

echo "✅ Backend setup complete"

# Setup Frontend
echo ""
echo "🎨 Setting up Frontend..."
cd ../frontend

# Install Node.js dependencies
npm install

echo "✅ Frontend setup complete"

echo ""
echo "🎉 Project Nova setup complete!"
echo ""
echo "To start the application:"
echo "1. Backend: cd backend && python main.py"
echo "2. Frontend: cd frontend && npm start"
echo ""
echo "Access the application at http://localhost:3000"
