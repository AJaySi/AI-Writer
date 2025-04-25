@echo off
:: ALwrity Automated Windows Installer
:: This script will set up ALwrity with minimal user input.
:: Last updated: April 23, 2025

chcp 65001 >nul
setlocal enabledelayedexpansion

:: Welcome message
cls
echo ======================================
echo   ALwrity - One Click Windows Installer
echo ======================================
echo.

:: Check for admin rights
openfiles >nul 2>&1
if %errorlevel% NEQ 0 (
    echo This installer needs to be run as administrator.
    echo Please right-click and select "Run as administrator".
    pause
    exit /b 1
)

:: Check if Python 3.11 is installed
python --version 2>nul | findstr /i "3.11" >nul
if errorlevel 1 (
    echo Python 3.11 is not installed or not in PATH.
    echo Downloading Python 3.11 installer...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe -OutFile python-3.11.6-amd64.exe"
    echo Launching Python installer. Please check 'Add Python to PATH' and complete installation.
    start python-3.11.6-amd64.exe
    echo After installation, please re-run this installer.
    pause
    exit /b 1
)

:: Check for Visual C++ Build Tools
where cl >nul 2>&1
if errorlevel 1 (
    echo Visual C++ Build Tools not found. Installing...
    powershell -Command "Start-Process 'powershell' -Verb runAs -ArgumentList 'winget install Microsoft.VisualStudio.2022.BuildTools --silent --override \"--wait --quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended\"'"
    echo Please wait for the installation to finish, then re-run this installer.
    pause
    exit /b 1
)

:: Check for Rust compiler
where rustc >nul 2>&1
if errorlevel 1 (
    echo Rust compiler not found. Installing...
    powershell -Command "Invoke-WebRequest -Uri https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe -OutFile rustup-init.exe"
    start rustup-init.exe -y
    echo Please wait for the installation to finish, then re-run this installer.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment and install requirements
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements if requirements.txt exists
if exist requirements.txt (
    echo Installing Python dependencies...
    pip install -r requirements.txt
)

:: Install ALwrity
if exist setup.py (
    echo Installing ALwrity...
    python setup.py install
) else (
    echo setup.py not found. Skipping ALwrity install step.
)

echo.
echo Installation complete!
echo To start ALwrity, open a new command prompt and type: alwrity
echo.
pause
