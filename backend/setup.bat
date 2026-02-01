@echo off
echo ========================================
echo SAFE ROUTE Backend Setup
echo ========================================
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Step 2: Checking environment configuration...
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and configure your database settings!
    echo.
)
echo.

echo Step 3: Creating upload directories...
if not exist uploads mkdir uploads
if not exist uploads\accidents mkdir uploads\accidents
if not exist logs mkdir logs
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your database credentials
echo 2. Create MySQL database: mysql -u root -p ^< schema.sql
echo 3. Run the application: python app.py
echo.
pause
