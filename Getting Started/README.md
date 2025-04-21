## Easy Installation Guide for Content Creators

### Step 1: Install Python 3.11
1. Download Python 3.11 installer:
   - Visit [Python 3.11.6 Download Page](https://www.python.org/downloads/release/python-3116/)
   - Scroll down and click on "Windows installer (64-bit)" 
   - Save the file to your computer

2. Run the installer:
   - Double click the downloaded file
   - ✅ IMPORTANT: Check "Add Python 3.11 to PATH"
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

### Step 2: Install ALwrity
1. Download this project:
   - Click the green "Code" button above
   - Select "Download ZIP"
   - Extract the ZIP file to your desired location

2. Open Command Prompt:
   - Press Windows + R
   - Type "cmd" and press Enter
   - Navigate to the extracted folder:
     ```
     cd path\to\ALwrity
     ```

3. Run the automatic installer:
   ```
   python setup.py install
   ```

### Troubleshooting
If you encounter any issues:
1. Make sure Python 3.11 is installed correctly:
   - Open Command Prompt
   - Type: `python --version`
   - Should show: `Python 3.11.x`

2. Common Issues:
   - If you see "Python is not recognized": Restart your computer
   - If you get package errors: Run `pip install --upgrade pip` first

Need help? [Open an issue](../../issues) and we'll assist you!

## For Developers
If you're a developer or want to contribute:
```bash
# Clone the repository
git clone https://github.com/yourusername/ALwrity.git

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

# ALwrity - AI Content Writing Assistant

## Quick Start Guide for Non-Technical Users

### Option 1: One-Click Installation (Recommended)
1. Download this project:
   - Click the green "Code" button above
   - Select "Download ZIP"
   - Extract the ZIP file to your desired location (e.g., Desktop)

2. Run the installer:
   - Double-click `install.bat` in the extracted folder
   - If Windows asks for permission, click "Yes"
   - Follow the on-screen instructions
   - Wait for the installation to complete

3. Start ALwrity:
   - Open Command Prompt (Windows + R, type "cmd", press Enter)
   - Navigate to the ALwrity folder:
     ```
     cd path\to\ALwrity
     ```
   - Type `alwrity` and press Enter

### Option 2: Manual Installation
If the one-click installer doesn't work, follow these steps:

1. Install Python 3.11:
   - Visit [Python 3.11.6 Download Page](https://www.python.org/downloads/release/python-3116/)
   - Click "Windows installer (64-bit)"
   - Run the installer
   - ✅ IMPORTANT: Check "Add Python 3.11 to PATH"
   - Click "Install Now"
   - Wait for installation to complete

2. Install ALwrity:
   - Open Command Prompt (Windows + R, type "cmd", press Enter)
   - Navigate to the ALwrity folder:
     ```
     cd path\to\ALwrity
     ```
   - Run the installation:
     ```
     python setup.py install
     ```
   - Follow any on-screen instructions

3. Start ALwrity:
   - In the same Command Prompt window, type:
     ```
     alwrity
     ```
   - Press Enter

### Troubleshooting Guide

#### Common Issues and Solutions:

1. "Python is not recognized"
   - Solution: Restart your computer after installing Python
   - Make sure you checked "Add Python 3.11 to PATH" during installation

2. "Visual C++ Build Tools not found"
   - Solution: Run this command in an administrative PowerShell:
     ```
     winget install Microsoft.VisualStudio.2022.BuildTools --silent --override "--wait --quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
     ```

3. "Rust compiler not found"
   - Solution: Run these commands in PowerShell:
     ```
     Invoke-WebRequest -Uri https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe -OutFile rustup-init.exe
     ./rustup-init.exe -y
     ```

4. Installation Errors
   - Check the `install_errors.log` file in the ALwrity folder
   - Share the error message with our support team

#### Need Help?
- Open an issue on GitHub
- Join our support community
- Contact our support team

### System Requirements
- Windows 10 or later
- Python 3.11.x
- At least 4GB RAM
- 2GB free disk space

### First-Time Setup
After installation:
1. The first time you run ALwrity, it will ask for your API keys
2. Follow the on-screen instructions to enter your keys
3. Your keys will be saved securely for future use

### Updating ALwrity
To update to the latest version:
1. Download the latest release
2. Run `install.bat` again
3. Follow the on-screen instructions