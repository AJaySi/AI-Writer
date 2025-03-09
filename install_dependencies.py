#!/usr/bin/env python3
"""
Installation helper script for AI-Writer
This script checks for required system dependencies and guides the user through installation
"""

import os
import sys
import platform
import subprocess
import shutil
import datetime
import socket
import traceback

def log_error(error_type, details):
    """
    Logs installation errors to a file with timestamp and system information.
    
    Args:
        error_type: Type of error (e.g., 'Python Version Check', 'Rust Installation')
        details: Detailed error message
    """
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'install_errors.log')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Collect system information
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.machine(),
        "Python Version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "Hostname": socket.gethostname()
    }
    
    # Format the log entry
    log_entry = f"[{timestamp}] ERROR: {error_type}\n"
    log_entry += f"Details: {details}\n"
    log_entry += "System Information:\n"
    for key, value in system_info.items():
        log_entry += f"  {key}: {value}\n"
    log_entry += "-" * 80 + "\n"
    
    # Write to log file
    with open(log_file, 'a') as f:
        f.write(log_entry)
    
    print(f"Error logged to {log_file}")

def check_python_version():
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        error_msg = f"Python 3.10+ is required. Found Python {version.major}.{version.minor}"
        print(f"Error: {error_msg}")
        log_error("Python Version Check", error_msg)
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} found")
    return True

def check_visual_cpp_build_tools():
    if platform.system() != "Windows":
        return True
    
    print("Checking for Visual C++ Build Tools...")
    
    # Check if cl.exe exists in PATH
    if shutil.which("cl"):
        print("✓ Visual C++ Build Tools found")
        return True
    
    error_msg = "Visual C++ Build Tools not found. Required for building certain Python packages."
    print("❌ Visual C++ Build Tools not found")
    print("\nVisual C++ Build Tools are required to build certain Python packages.")
    print("To install Visual C++ Build Tools:")
    print("Option 1: Run this command in an administrative PowerShell:")
    print("  winget install Microsoft.VisualStudio.2022.BuildTools --silent --override \"--wait --quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended\"")
    print("\nOption 2: Download and install from the official Microsoft website:")
    print("  https://visualstudio.microsoft.com/visual-cpp-build-tools/")
    
    log_error("Visual C++ Build Tools Check", error_msg)
    return False

def check_rust_compiler():
    print("Checking for Rust compiler...")
    
    # Check if rustc exists in PATH
    if shutil.which("rustc"):
        print("✓ Rust compiler found")
        return True
    
    error_msg = "Rust compiler not found. Required for building certain Python packages."
    print("❌ Rust compiler not found")
    if platform.system() == "Windows":
        print("\nTo install Rust on Windows, run:")
        print("  Invoke-WebRequest -Uri https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe -OutFile rustup-init.exe")
        print("  ./rustup-init.exe -y")
    else:
        print("\nTo install Rust on Linux/macOS, run:")
        print("  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
        print("  source $HOME/.cargo/env")
    
    log_error("Rust Compiler Check", error_msg)
    return False

def main():
    print("AI-Writer Dependency Checker\n")
    
    all_checks_passed = True
    
    # Run dependency checks
    if not check_python_version():
        all_checks_passed = False
    
    if not check_visual_cpp_build_tools():
        all_checks_passed = False
    
    if not check_rust_compiler():
        all_checks_passed = False
    
    # If all checks pass, create virtual environment and install requirements
    if all_checks_passed:
        print("\nAll system dependencies found!")
        
        # Ask user if they want to proceed with installation
        response = input("\nWould you like to create a virtual environment and install Python dependencies? (y/n): ")
        if response.lower() == 'y':
            print("\nCreating virtual environment...")
            try:
                if platform.system() == "Windows":
                    venv_result = os.system("python -m venv venv")
                    if venv_result != 0:
                        raise Exception(f"Failed to create virtual environment, exit code: {venv_result}")
                    install_result = os.system("venv\\Scripts\\activate && pip install -r requirements.txt")
                    if install_result != 0:
                        raise Exception(f"Failed to install dependencies, exit code: {install_result}")
                else:
                    venv_result = os.system("python3 -m venv venv")
                    if venv_result != 0:
                        raise Exception(f"Failed to create virtual environment, exit code: {venv_result}")
                    install_result = os.system("source venv/bin/activate && pip install -r requirements.txt")
                    if install_result != 0:
                        raise Exception(f"Failed to install dependencies, exit code: {install_result}")
            except Exception as e:
                error_msg = str(e)
                print(f"\nError during installation: {error_msg}")
                log_error("Dependency Installation", f"{error_msg}\n{traceback.format_exc()}")
                print("Please check the install_errors.log file for details.")
            
            print("\nInstallation complete! To run the application:")
            print("1. Activate the virtual environment:")
            if platform.system() == "Windows":
                print("   venv\\Scripts\\activate")
            else:
                print("   source venv/bin/activate")
            print("2. Run the application:")
            print("   streamlit run alwrity.py")
        else:
            print("\nSkipping dependency installation. You can install them manually with:")
            print("1. Create a virtual environment: python -m venv venv")
            print("2. Activate the virtual environment")
            print("3. Install dependencies: pip install -r requirements.txt")
    else:
        print("\nPlease install the missing dependencies and try again.")
        print("Check the install_errors.log file for detailed error information.")
if __name__ == "__main__":
    main()