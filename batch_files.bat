@echo off
echo ========================================
echo Doctor Preferences Converter
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Working in: %CD%
echo.
echo Converting markdown files to HTML...
echo.

python convert_doctor_data.py

echo.
echo ========================================
echo Done! Press any key to close...
pause >nul


@echo off
echo ========================================
echo Doctor Preferences Network Server
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Working in: %CD%
echo.
echo Starting NETWORK web server...
echo Other computers can access this server.
echo.
echo IMPORTANT: Keep this window open!
echo To stop the server, close this window or press Ctrl+C
echo ========================================
echo.

python start_network_server.py