@echo off
echo Starting AI Judiciary Platform Backend...
echo =====================================

cd backend

echo Installing dependencies...
py -m pip install -r requirements.txt

echo Running migrations...
py manage.py migrate

echo Starting Django server...
echo Backend will be available at: http://localhost:8000
echo Admin panel: http://localhost:8000/admin
echo Health check: http://localhost:8000/api/auth/health/
echo.
echo Press Ctrl+C to stop the server
echo.

py manage.py runserver