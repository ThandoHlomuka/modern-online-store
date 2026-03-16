@echo off
REM Modern Online Store - Run Script for Windows
REM This script starts the Flask development server

echo.
echo ====================================================================
echo   Modern Online Store - Development Server
echo ====================================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found
    echo Please create .env file with your configuration
    echo Copy .env.example to .env and edit it
    pause
)

echo Starting Flask development server...
echo.
echo Open your browser and navigate to:
echo   http://localhost:5000
echo.
echo Admin Dashboard:
echo   http://localhost:5000/admin
echo   Username: ThandoHlomuka
echo   Password: Nozibusiso89
echo.
echo Press Ctrl+C to stop the server
echo ====================================================================
echo.

python app.py
