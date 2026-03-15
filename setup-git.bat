@echo off
echo =====================================
echo   Git Repository Setup
echo =====================================
echo.

REM Check if git is already initialized
if exist ".git" (
    echo Git repository already initialized.
    echo.
) else (
    echo Initializing Git repository...
    git init
    echo.
)

REM Configure git user (if not configured)
git config user.name >nul 2>&1
if errorlevel 1 (
    echo Setting up Git user...
    set /p gitname="Enter your GitHub username: "
    git config user.name "%gitname%"
    
    set /p gitemail="Enter your GitHub email: "
    git config user.email "%gitemail%"
    echo.
)

REM Initial commit
echo Creating initial commit...
git add .
git commit -m "Initial commit: Modern Online Store"
echo.

echo =====================================
echo   Setup Complete!
echo =====================================
echo.
echo Next steps:
echo 1. Create a new repository on GitHub (do not initialize with README)
echo 2. Copy the commands from GitHub to connect your repository
echo.
echo Example:
echo   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
echo   git branch -M main
echo   git push -u origin main
echo.
echo Or run 'deploy.bat' after setting up the remote.
echo.
pause
