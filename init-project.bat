@echo off
REM DNS Bot v2 - Project Initialization Script (Batch wrapper)

setlocal enabledelayedexpansion

cls
echo.
echo ===== DNS Bot v2 - Project Initialization =====
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo X Python is not installed
        echo Install from: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    set PY=python3
) else (
    set PY=python
)

echo + Python is available
echo.
echo Running initialization script...
echo.

REM Run the initialization script
%PY% init-project.py

if errorlevel 1 (
    echo.
    echo X Initialization failed
    pause
    exit /b 1
)

echo.
echo ===== Initialization completed successfully! =====
echo.
echo Next steps:
echo 1. Edit backend\.env and add your API keys
echo 2. Run: setup.bat to start services
echo.
pause
