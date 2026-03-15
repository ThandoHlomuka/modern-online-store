@echo off
echo =====================================
echo   GitHub Push ^& Vercel Deploy
echo =====================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo.
)

REM Check if remote is set
git remote -v | findstr origin >nul
if errorlevel 1 (
    echo No remote repository configured.
    echo.
    echo Please create a repository on GitHub, then run:
    echo git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
    echo.
    pause
    exit /b
)

REM Add all files
echo Adding files to git...
git add .
echo.

REM Commit
echo Enter commit message (or press Enter for default):
set /p commitmsg="Commit message: "
if "%commitmsg%"=="" set commitmsg=Update project

git commit -m "%commitmsg%"
echo.

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main
if errorlevel 1 (
    echo Push failed. Trying with 'master' branch...
    git branch -M master
    git push -u origin master
)
echo.

echo =====================================
echo   Push Complete!
echo =====================================
echo.
echo Next steps:
echo 1. Go to https://vercel.com
echo 2. Click "Add New Project"
echo 3. Import your GitHub repository
echo 4. Click "Deploy"
echo.
echo Your project will be live at: https://your-project.vercel.app
echo.
pause
