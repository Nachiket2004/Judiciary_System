@echo off
echo Starting AI Judiciary Platform Frontend...
echo =========================================

cd frontend

echo Getting Flutter dependencies...
flutter pub get

echo Starting Flutter web server...
echo Frontend will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

flutter run -d web-server --web-port 3000