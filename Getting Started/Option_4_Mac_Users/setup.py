import sys
import os
import subprocess
import shutil
from pathlib import Path

def print_step(text):
    print(f"\n→ {text}")

def print_error(text):
    print(f"\nError: {text}", file=sys.stderr)

def check_homebrew():
    try:
        subprocess.run(['brew', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def setup_homebrew():
    print_step("Homebrew is required for some dependencies")
    print("Please install Homebrew by running this command in Terminal:")
    print('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
    print("\nAfter installing Homebrew, run this setup script again.")
    sys.exit(1)

def create_virtual_environment(venv_path):
    try:
        if venv_path.exists():
            shutil.rmtree(venv_path)
        subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
        return True
    except Exception as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False

def install_requirements(venv_python, requirements_path):
    try:
        subprocess.run([str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        subprocess.run([str(venv_python), '-m', 'pip', 'install', '-r', str(requirements_path)], check=True)
        return True
    except Exception as e:
        print_error(f"Failed to install requirements: {e}")
        return False

def main():
    print("\n=== ALwrity Mac Installation ===\n")
    
    if not check_homebrew():
        setup_homebrew()
    
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    requirements_path = project_root / 'requirements.txt'
    venv_path = current_dir / 'venv'
    
    print_step("Creating virtual environment")
    if not create_virtual_environment(venv_path):
        return
    
    print_step("Installing dependencies")
    venv_python = venv_path / 'bin' / 'python'
    if not install_requirements(venv_python, requirements_path):
        return
    
    print("\n✓ Installation completed successfully!")
    print("\nTo start ALwrity:")
    print("1. Open Terminal in this directory")
    print("2. Run: source venv/bin/activate")
    print("3. Run: streamlit run alwrity.py")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nInstallation cancelled")
    except Exception as e:
        print_error(f"Unexpected error: {e}")