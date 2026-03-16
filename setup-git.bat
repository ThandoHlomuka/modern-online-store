@echo off
REM Modern Online Store - Git Setup Script for Windows
REM This script initializes Git and prepares for deployment

echo.
echo ====================================================================
echo   Modern Online Store - Git Setup
echo   Preparing for Vercel deployment
echo ====================================================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com
    pause
    exit /b 1
)

echo [OK] Git found
echo.

REM Initialize Git repository if not already initialized
if not exist ".git\" (
    echo Initializing Git repository...
    git init
    echo [OK] Git repository initialized
) else (
    echo [OK] Git repository already exists
)
echo.

REM Check if .env is in .gitignore
findstr /C:".env" .gitignore >nul 2>&1
if errorlevel 1 (
    echo [WARNING] .env is not in .gitignore
    echo Adding .env to .gitignore...
    echo .env >> .gitignore
) else (
    echo [OK] .env is properly ignored
)
echo.

REM Create .gitignore if it doesn't exist
if not exist ".gitignore" (
    echo Creating .gitignore...
    echo .env >> .gitignore
    echo __pycache__/ >> .gitignore
    echo *.pyc >> .gitignore
    echo venv/ >> .gitignore
    echo .env >> .gitignore
    echo [OK] .gitignore created
)
echo.

REM Show status
echo Current Git status:
git status
echo.

echo ====================================================================
echo   Next Steps for GitHub Deployment:
echo ====================================================================
echo.
echo 1. Create a new repository on GitHub
echo 2. Run these commands:
echo.
echo    git add .
echo    git commit -m "Initial commit - Modern Online Store"
echo    git branch -M main
echo    git remote add origin https://github.com/YOUR_USERNAME/modern-online-store.git
echo    git push -u origin main
echo.
echo 3. Go to Vercel and import your GitHub repository
echo 4. Set environment variables in Vercel dashboard
echo.
echo For detailed instructions, see DEPLOYMENT.md
echo.
pause
