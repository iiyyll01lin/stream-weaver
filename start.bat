@echo off
REM Phase 1 Service Startup Script (Windows)
REM Quick Start Script for Phase 1

echo ==================================
echo Line Balance System Phase 1 Launcher
echo Line Balance System - Phase 1
echo ==================================
echo.

REM Check if Python is installed
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Cannot find Python
    echo Please install Python 3.10+ and try again
    pause
    exit /b 1
)

python --version
echo.

REM Check dependencies
echo Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo ! Dependencies not installed
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo √ Dependencies ready
echo.

REM Check data files
echo Checking data files...
if not exist "data\test_tasks.csv" (
    echo X Cannot find data\test_tasks.csv
    echo Please ensure data files exist
    pause
    exit /b 1
)

echo √ Data files exist
echo.

REM Create output directory
if not exist "output" mkdir output

REM Start service
echo ==================================
echo Starting API service...
echo ==================================
echo.
echo Service URL: http://localhost:8000
echo API Documentation: http://localhost:8000/api/docs
echo.
echo Press Ctrl+C to stop service
echo.

python src\api_server.py
