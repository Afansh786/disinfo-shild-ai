@echo off
setlocal enabledelayedexpansion
title DisinfoShield AI 2026 - Master Launcher
cd /d "%~dp0"

echo ==============================================================
echo   Disinfo Shield AI 2026 - Starting Dashboard and Backend
echo ==============================================================
echo.

:: 1. Check direct Python 3.11 path
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    echo [*] Found Python 3.11: %LOCALAPPDATA%\Programs\Python\Python311\python.exe
    echo [*] Starting server and opening dashboard at http://127.0.0.1:8000
    echo.
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" run.py
    if %errorlevel% equ 0 goto :eof
)

:: 2. Check py.exe launcher
where py >nul 2>nul
if %errorlevel% equ 0 (
    echo [*] Found Python launcher: py.exe
    echo [*] Starting server and opening dashboard at http://127.0.0.1:8000
    echo.
    py run.py
    if %errorlevel% equ 0 goto :eof
)

:: 3. Check python.exe in PATH
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo [*] Found Python executable: python.exe
    echo [*] Starting server and opening dashboard at http://127.0.0.1:8000
    echo.
    python run.py
    if %errorlevel% equ 0 goto :eof
)

:: 4. Fallback: Launch standalone HTML dashboard directly in default browser
echo.
echo [INFO] Opening standalone UI directly in default browser...
start "" "%~dp0desktop_app.html"
exit /b 0
