@echo off
setlocal enabledelayedexpansion

s :: Set colors for better visibility
color 0A

:: Set the Python version requirement
set MIN_PYTHON_VERSION=3.9

echo ===============================================
echo           ALwrity Installation Setup
echo ===============================================
echo.

echo [1/5] Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is not installed!
    echo Please install Python %MIN_PYTHON_VERSION% or higher from python.org
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%V in ('python --version 2^>^&1') do set PYTHON_VERSION=%%V
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

:: Check Python version
set /a PYTHON_VER=%PYTHON_MAJOR%*100 + %PYTHON_MINOR%
set /a MIN_VER=309
if %PYTHON_VER% LSS %MIN_VER% (
    color 0C
    echo [ERROR] Python version %MIN_PYTHON_VERSION% or higher is required!
    echo Current version: %PYTHON_VERSION%
    echo Please upgrade Python from python.org
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

echo [✓] Python %PYTHON_VERSION% detected
echo.

echo [2/5] Creating virtual environment...
python -m venv "%~dp0..\..\venv"
if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to create virtual environment!
    echo Press any key to exit...
    pause > nul
    exit /b 1
)
echo [✓] Virtual environment created
echo.

echo [3/5] Activating virtual environment...
call "%~dp0..\..\venv\Scripts\activate.bat"
if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to activate virtual environment!
    echo Press any key to exit...
    pause > nul
    exit /b 1
)
echo [✓] Virtual environment activated
echo.

echo [4/5] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to upgrade pip!
    echo Press any key to exit...
    pause > nul
    exit /b 1
)
echo [✓] Pip upgraded
echo.

echo [5/5] Installing requirements...
pip install -r "%~dp0..\..\requirements.txt"
if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to install requirements!
    echo Press any key to exit...
    pause > nul
    exit /b 1
)
echo [✓] Requirements installed
echo.

color 0A
echo ===============================================
echo       Installation Completed Successfully!
echo ===============================================
echo.
echo Next steps to run ALwrity:
echo.
echo 1. Open a new Command Prompt window
echo 2. Navigate to the ALwrity root directory by copying and pasting this command:
echo    cd /d "%~dp0..\.."
echo.
echo 3. Activate the virtual environment by copying and pasting this command:
echo    "%~dp0..\..\venv\Scripts\activate.bat"
echo.
echo 4. Run ALwrity with Streamlit by copying and pasting this command:
echo    streamlit run "%~dp0..\..\alwrity.py"
echo.
echo Note: You'll need to activate the virtual environment (step 3)
echo       each time you want to run ALwrity.
echo.
echo Troubleshooting:
echo - If you see any errors, make sure Python is in your PATH
echo - For help, visit: https://github.com/yourusername/ALwrity
echo.
echo Press any key to exit...
pause > nul