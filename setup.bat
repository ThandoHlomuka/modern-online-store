@echo off
REM Modern Online Store - Setup Script for Windows
REM This script sets up the local development environment

echo.
echo ====================================================================
echo   Modern Online Store - Setup Script
echo   Setting up local development environment
echo ====================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo [OK] Dependencies installed
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo [OK] .env file created
    echo.
    echo [!] IMPORTANT: Edit .env and add your Supabase credentials
    echo     - SUPABASE_URL
    echo     - SUPABASE_KEY
    echo     - SUPABASE_DB_URL
    echo.
) else (
    echo [OK] .env file already exists
)
echo.

REM Create necessary directories
if not exist "static\images\" mkdir static\images
if not exist "logs\" mkdir logs

echo ====================================================================
echo   Setup Complete!
echo ====================================================================
echo.
echo Next steps:
echo 1. Edit .env file with your Supabase credentials
echo 2. Run the database schema in Supabase SQL Editor
echo 3. Run: run.bat to start the development server
echo.
echo For deployment instructions, see DEPLOYMENT.md
echo.
pause
