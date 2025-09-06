# Project Nova - Quick Start Guide

## 🚀 Automated Startup Scripts

I've created **3 different startup scripts** that will automatically set up and run Project Nova for you:

### For Windows Users:

#### Option 1: Batch File (Recommended)
```bash
# Double-click this file or run in Command Prompt:
start-nova.bat
```

#### Option 2: PowerShell Script
```powershell
# Right-click and "Run with PowerShell" or run in PowerShell:
.\start-nova.ps1
```

### For Linux/Mac Users:
```bash
# Make executable and run:
chmod +x start-nova.sh
./start-nova.sh
```

## 🎯 What These Scripts Do:

1. **Check Prerequisites** - Verify Python and Node.js are installed
2. **Install Dependencies** - Automatically install required packages
3. **Train ML Model** - Create the credit scoring model (if not exists)
4. **Start Backend** - Launch FastAPI server on http://localhost:8000
5. **Start Frontend** - Launch React app on http://localhost:3000
6. **Open Separate Windows** - Each service runs in its own terminal window

## 💡 How to Use:

### For Windows:
1. Navigate to: `D:\Chirag\Program\grabhack\project-nova\`
2. Double-click `start-nova.bat`
3. Follow the prompts
4. Two new windows will open (backend + frontend)
5. Your browser should automatically open to http://localhost:3000

### What You'll See:
```
================================================================
🚀 PROJECT NOVA - EQUITABLE CREDIT SCORING ENGINE
================================================================
Starting automated setup...

✅ Python found: Python 3.10.6
✅ Node.js found: v22.14.0
🔧 Setting up backend environment...
✅ ML model already exists
🎨 Setting up frontend environment...
✅ Node.js packages already installed
🚀 Starting Project Nova...

Backend will start on: http://localhost:8000
Frontend will start on: http://localhost:3000
```

## 🛑 How to Stop:

- **Close the terminal windows** that opened for backend and frontend
- Or press **Ctrl+C** in each terminal window

## 🔧 Troubleshooting:

If something goes wrong:
1. Make sure you're running the script from the correct directory
2. Check that Python and Node.js are installed
3. Run the manual commands from my previous instructions

## ⚡ Quick Test:

After running the script, visit:
- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

That's it! Now you can start Project Nova with just **one click**! 🎉
