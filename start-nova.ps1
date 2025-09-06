# Project Nova - PowerShell Startup Script
# This script starts both backend and frontend automatically

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "🚀 PROJECT NOVA - EQUITABLE CREDIT SCORING ENGINE" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Starting automated setup..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.8+ first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 14+ first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Navigate to project directory
$projectPath = "D:\Chirag\Program\grabhack\project-nova"
Set-Location $projectPath

# Verify we're in the right directory
if (-not (Test-Path "backend\main.py")) {
    Write-Host "❌ Cannot find backend\main.py. Please check if you're in the correct directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "frontend\package.json")) {
    Write-Host "❌ Cannot find frontend\package.json. Please check if you're in the correct directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "🔧 Setting up backend environment..." -ForegroundColor Yellow
Set-Location "backend"

# Install Python dependencies
Write-Host "Installing Python packages..." -ForegroundColor Cyan
pip install fastapi==0.104.1 uvicorn==0.24.0 pandas==2.1.3 scikit-learn==1.3.2 pydantic==2.5.0 python-multipart==0.0.6 joblib==1.3.2 requests==2.31.0 | Out-Null

# Check if model exists, if not train it
if (-not (Test-Path "credit_model.pkl")) {
    Write-Host "🧠 Training ML model..." -ForegroundColor Magenta
    python train_model.py
} else {
    Write-Host "✅ ML model already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎨 Setting up frontend environment..." -ForegroundColor Yellow
Set-Location "..\frontend"

# Install Node.js dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node.js packages..." -ForegroundColor Cyan
    npm install | Out-Null
} else {
    Write-Host "✅ Node.js packages already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting Project Nova..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Backend will start on: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend will start on: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue"

# Start backend in a new PowerShell window
Write-Host "Starting backend server..." -ForegroundColor Green
$backendPath = "D:\Chirag\Program\grabhack\project-nova\backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; python main.py" -WindowStyle Normal

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend in a new PowerShell window
Write-Host "Starting frontend server..." -ForegroundColor Green
$frontendPath = "D:\Chirag\Program\grabhack\project-nova\frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm start" -WindowStyle Normal

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "🎉 PROJECT NOVA IS STARTING!" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend: http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Both servers are starting in separate windows." -ForegroundColor Cyan
Write-Host "Close those windows to stop the servers." -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit this script"
