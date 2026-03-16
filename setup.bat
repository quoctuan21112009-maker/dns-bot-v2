@echo off
REM Color codes for Windows (using title for visual feedback)
setlocal enabledelayedexpansion

echo.
echo ===== DNS Bot v2 - Local Setup Script =====
echo.

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Docker is not installed
    echo Install from: https://www.docker.com/products/docker-desktop
    exit /b 1
)
echo + Docker is installed

REM Check Docker Compose
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Docker Compose is not installed
    exit /b 1
)
echo + Docker Compose is installed
echo.

REM Create .env files
echo Creating backend .env file...
if not exist "backend\.env" (
    copy backend\.env.example backend\.env
    echo + Created backend\.env
) else (
    echo ! backend\.env already exists
)

echo Creating frontend .env file...
if not exist "frontend\.env" (
    copy frontend\.env.example frontend\.env
    echo + Created frontend\.env
) else (
    echo ! frontend\.env already exists
)

echo.
echo Starting services...
echo.

REM Start Docker Compose
docker-compose up -d

REM Wait for services
echo.
echo Waiting for services to start...
timeout /t 10 /nobreak

echo.
echo ===== Service Status =====
docker-compose ps

echo.
echo ===== URLs =====
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo PostgreSQL: localhost:5432
echo Redis: localhost:6379

echo.
echo ===== Next Steps =====
echo 1. Set your API keys in backend\.env
echo 2. Access the application at http://localhost:5173
echo 3. View logs: docker-compose logs -f
echo 4. Stop services: docker-compose down

echo.
echo Setup complete!
echo.

endlocal
