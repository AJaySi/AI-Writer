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

def check_python_version():
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"Error: Python 3.10+ is required. Found Python {version.major}.{version.minor}")
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
    
    print("❌ Visual C++ Build Tools not found")
    print("\nVisual C++ Build Tools are required to build certain Python packages.")
    print("To install Visual C++ Build Tools:")
    print("Option 1: Run this command in an administrative PowerShell:")
    print("  winget install Microsoft.VisualStudio.2022.BuildTools --silent --override \"--wait --quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended\"")
    print("\nOption 2: Download and install from the official Microsoft website:")
    print("  https://visualstudio.microsoft.com/visual-cpp-build-tools/")
    
    return False

def check_rust_compiler():
    print("Checking for Rust compiler...")
    
    # Check if rustc exists in PATH
    if shutil.which("rustc"):
        print("✓ Rust compiler found")
        return True
    
    print("❌ Rust compiler not found")
    if platform.system() == "Windows":
        print("\nTo install Rust on Windows, run:")
        print("  Invoke-WebRequest -Uri https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe -OutFile rustup-init.exe")
        print("  ./rustup-init.exe -y")
    else:
        print("\nTo install Rust on Linux/macOS, run:")
        print("  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
        print("  source $HOME/.cargo/env")
    
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
            if platform.system() == "Windows":
                os.system("python -m venv venv")
                os.system("venv\\Scripts\\activate && pip install -r requirements.txt")
            else:
                os.system("python3 -m venv venv")
                os.system("source venv/bin/activate && pip install -r requirements.txt")
            
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

if __name__ == "__main__":
    main()