@echo off
REM Force Clean Vercel Deployment Script
REM This script clears local cache and forces a fresh deployment

echo ========================================
echo   Force Clean Vercel Deployment
echo ========================================
echo.

REM Clear local Vercel cache
echo [1/4] Clearing Vercel cache...
if exist ".vercel\cache" (
    rmdir /s /q ".vercel\cache"
    echo   - Cleared .vercel\cache
) else (
    echo   - No cache to clear
)

REM Clear Python cache
echo [2/4] Clearing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del /s /q "%%f"
for /r . %%f in (*.pyo) do @if exist "%%f" del /s /q "%%f"
echo   - Cleared Python cache files

REM Clear egg-info
echo [3/4] Clearing egg-info...
for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"
echo   - Cleared egg-info

REM Check git status
echo [4/4] Checking git status...
git status --short
echo.

echo ========================================
echo   Deployment Files Ready
echo ========================================
echo.
echo Next steps:
echo   1. Commit changes: git add . && git commit -m "chore: force clean vercel build"
echo   2. Push to GitHub: git push
echo   3. Vercel will auto-deploy with fresh build
echo.
echo OR manually trigger:
echo   vercel --prod
echo.
pause
