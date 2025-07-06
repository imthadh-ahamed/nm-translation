@echo off
REM Development startup script for Windows

echo Starting Neural Machine Translation System...

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is required but not installed.
    exit /b 1
)

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Node.js is required but not installed.
    exit /b 1
)

echo Installing backend dependencies...
cd backend
pip install -r requirements.txt

echo Starting backend server...
start /B python -m app.main

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

echo Installing frontend dependencies...
cd ..\frontend
call npm install

echo Starting frontend server...
start /B npm run dev

echo.
echo 🚀 Neural Machine Translation System is starting...
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop all services
pause >nul

REM Kill processes (basic cleanup)
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul
