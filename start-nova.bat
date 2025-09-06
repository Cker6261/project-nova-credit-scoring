@echo off
REM Project Nova - Automated Startup Script
REM This script starts both backend and frontend automatically

echo.
echo ================================================================
echo 🚀 PROJECT NOVA - EQUITABLE CREDIT SCORING ENGINE
echo ================================================================
echo Starting automated setup...
echo.

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
echo.

REM Navigate to project directory
cd /d "D:\Chirag\Program\grabhack\project-nova"

REM Check if we're in the right directory
if not exist "backend\main.py" (
    echo ❌ Cannot find backend\main.py. Please check if you're running this from the correct directory.
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo ❌ Cannot find frontend\package.json. Please check if you're running this from the correct directory.
    pause
    exit /b 1
)

echo 🔧 Setting up backend environment...
cd backend

REM Install Python dependencies if needed
echo Installing Python packages...
pip install fastapi==0.104.1 uvicorn==0.24.0 pandas==2.1.3 scikit-learn==1.3.2 pydantic==2.5.0 python-multipart==0.0.6 joblib==1.3.2 requests==2.31.0 >nul 2>&1

REM Check if model exists, if not train it
if not exist "credit_model.pkl" (
    echo 🧠 Training ML model...
    python train_model.py
) else (
    echo ✅ ML model already exists
)

echo.
echo 🎨 Setting up frontend environment...
cd ..\frontend

REM Install Node.js dependencies if needed
if not exist "node_modules" (
    echo Installing Node.js packages...
    npm install >nul 2>&1
) else (
    echo ✅ Node.js packages already installed
)

echo.
echo 🚀 Starting Project Nova...
echo.
echo Backend will start on: http://localhost:8000
echo Frontend will start on: http://localhost:3000
echo.
echo Press any key to continue...
pause >nul

REM Start backend in a new window
echo Starting backend server...
start "Project Nova Backend" cmd /c "cd /d D:\Chirag\Program\grabhack\project-nova\backend && python main.py && pause"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window  
echo Starting frontend server...
start "Project Nova Frontend" cmd /c "cd /d D:\Chirag\Program\grabhack\project-nova\frontend && npm start && pause"

echo.
echo ================================================================
echo 🎉 PROJECT NOVA IS STARTING!
echo ================================================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Both servers are starting in separate windows.
echo Close those windows to stop the servers.
echo.
echo Press any key to exit this script...
pause >nul
