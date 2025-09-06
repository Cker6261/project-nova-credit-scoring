@echo off
REM Project Nova Setup Script for Windows
REM This script sets up the entire project for development

echo 🚀 Setting up Project Nova - Equitable Credit Scoring Engine
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 14+ first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Setup Backend
echo.
echo 🔧 Setting up Backend...
cd backend

REM Create virtual environment
python -m venv nova_env
call nova_env\Scripts\activate

REM Install Python dependencies
pip install -r requirements.txt

REM Train the ML model
echo 🧠 Training ML model...
python train_model.py

echo ✅ Backend setup complete

REM Setup Frontend
echo.
echo 🎨 Setting up Frontend...
cd ..\frontend

REM Install Node.js dependencies
npm install

echo ✅ Frontend setup complete

echo.
echo 🎉 Project Nova setup complete!
echo.
echo To start the application:
echo 1. Backend: cd backend ^&^& python main.py
echo 2. Frontend: cd frontend ^&^& npm start
echo.
echo Access the application at http://localhost:3000
pause
