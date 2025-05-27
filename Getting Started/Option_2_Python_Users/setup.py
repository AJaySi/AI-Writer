import sys
import os
import platform
import subprocess
import shutil
import datetime
import socket
import traceback
import pkg_resources
from setuptools import setup, find_packages

def log_error(error_type, details):
    """
    Logs installation errors to a file with timestamp and system information.
    """
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'install_errors.log')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.machine(),
        "Python Version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "Hostname": socket.gethostname()
    }
    
    log_entry = f"[{timestamp}] ERROR: {error_type}\n"
    log_entry += f"Details: {details}\n"
    log_entry += "System Information:\n"
    for key, value in system_info.items():
        log_entry += f"  {key}: {value}\n"
    log_entry += "-" * 80 + "\n"
    
    with open(log_file, 'a') as f:
        f.write(log_entry)
    
    print(f"Error logged to {log_file}")

def check_system_dependencies():
    """Check for required system dependencies."""
    print("Checking system dependencies...")
    all_checks_passed = True

    # User message about system dependencies
    print("\nNOTE: Some dependencies like Rust, Visual C++ Build Tools, or Python itself cannot be installed automatically by this script.")
    print("This is because installing system-level packages requires admin rights and can differ across operating systems.")
    print("For your safety and system stability, please follow the on-screen instructions to install any missing prerequisites manually.\n")

    # Check Python version
    print("Checking Python version...")
    if sys.version_info < (3, 11) or sys.version_info >= (3, 12):
        error_msg = "ALwrity requires Python 3.11.x"
        print(f"Error: {error_msg}")
        log_error("Python Version Check", error_msg)
        all_checks_passed = False
    else:
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} found")

    # Check Visual C++ Build Tools on Windows
    if platform.system() == "Windows":
        print("Checking for Visual C++ Build Tools...")
        if not shutil.which("cl"):
            error_msg = "Visual C++ Build Tools not found"
            print("❌ Visual C++ Build Tools not found")
            print("\nTo install Visual C++ Build Tools, run in an administrative PowerShell:")
            print("winget install Microsoft.VisualStudio.2022.BuildTools --silent --override \"--wait --quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended\"")
            log_error("Visual C++ Build Tools Check", error_msg)
            all_checks_passed = False
        else:
            print("✓ Visual C++ Build Tools found")

    # Check Rust compiler
    print("Checking for Rust compiler...")
    if not shutil.which("rustc"):
        error_msg = "Rust compiler not found"
        print("❌ Rust compiler not found")
        if platform.system() == "Windows":
            print("\nTo install Rust on Windows, run:")
            print("Invoke-WebRequest -Uri https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe -OutFile rustup-init.exe")
            print("./rustup-init.exe -y")
        else:
            print("\nTo install Rust on Linux/macOS, run:")
            print("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
            print("source $HOME/.cargo/env")
        log_error("Rust Compiler Check", error_msg)
        all_checks_passed = False
    else:
        print("✓ Rust compiler found")

    return all_checks_passed

def get_requirements():
    """Read requirements from requirements.txt."""
    with open('requirements.txt') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return requirements

def install_requirements(requirements):
    """Install each requirement, showing progress."""
    print("Installing required packages...")
    for requirement in requirements:
        try:
            print(f"Installing {requirement}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
        except subprocess.CalledProcessError as e:
            error_msg = f"Error installing {requirement}: {e}"
            print(error_msg)
            log_error("Package Installation", error_msg)
            sys.exit(1)

def main():
    """Main installation function."""
    print("ALwrity Installation\n")
    
    # Check system dependencies
    if not check_system_dependencies():
        print("\nPlease install the missing dependencies and try again.")
        print("Check the install_errors.log file for detailed error information.")
        sys.exit(1)

    # Create virtual environment if it doesn't exist
    if not os.path.exists("venv"):
        print("\nCreating virtual environment...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to create virtual environment: {e}"
            print(error_msg)
            log_error("Virtual Environment Creation", error_msg)
            sys.exit(1)

    # Activate virtual environment automatically (Linux/macOS only)
    if platform.system() != "Windows":
        activate_script = os.path.join("venv", "bin", "activate_this.py")
        if os.path.exists(activate_script):
            with open(activate_script) as f:
                exec(f.read(), {'__file__': activate_script})

    # Install requirements
    requirements = get_requirements()
    install_requirements(requirements)

    # Run setup
    setup(
        name="alwrity",
        version="1.0.0",
        description="AI-powered content writing assistant",
        author="Your Name",
        packages=find_packages(),
        python_requires=">=3.11, <3.12",
        install_requires=requirements,
        entry_points={
            'console_scripts': [
                'alwrity=alwrity:main',
            ],
        },
    )

    print("\nInstallation complete! To start ALwrity:")
    print("1. Activate the virtual environment:")
    if platform.system() == "Windows":
        print("   .\\venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run the application:")
    print("   streamlit run alwrity.py")
    print("\nYou can now use the 'alwrity' command as well.")

if __name__ == '__main__':
    main()