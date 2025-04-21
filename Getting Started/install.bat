@echo off
echo Welcome to ALwrity Installer
echo ============================
echo.

:: Check if Python 3.11 is installed
python --version 2>nul | findstr /i "3.11" >nul
if errorlevel 1 (
    echo Python 3.11 is not installed or not in PATH
    echo Please install Python 3.11 from https://www.python.org/downloads/release/python-3116/
    echo Make sure to check "Add Python 3.11 to PATH" during installation
    echo.
    echo Press any key to open the download page...
    pause >nul
    start https://www.python.org/downloads/release/python-3116/
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

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing ALwrity...
python setup.py install

echo.
echo Installation complete!
echo To start ALwrity, open a new command prompt and type: alwrity
echo.
pause 