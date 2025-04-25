# ALwrity Linux/macOS Installer Guide (`setup.py`)

---

## What is `setup.py`?
`setup.py` is an automated installer for ALwrity on Linux and macOS. It checks your system, sets up a virtual environment, installs all dependencies, and configures ALwrity for you.

---

## What Does It Do?
- Checks your Python version (must be 3.11.x)
- Checks for Rust compiler (required for some Python packages)
- Creates a Python virtual environment (`venv`) if it doesn't exist
- Activates the virtual environment (auto-activation for Linux/macOS)
- Installs all required Python packages from `requirements.txt`
- Installs ALwrity as a command-line tool
- Prints clear next steps for running ALwrity
- Logs any errors to `install_errors.log` for easy troubleshooting

---

## Prerequisites
- **Linux or macOS**
- **Python 3.11.x** (install from https://www.python.org/downloads/ if needed)
- **Rust compiler** (install with `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y`)
- **At least 4GB RAM**
- **2GB free disk space**

---

## Step-by-Step Instructions

### 1. Open a Terminal
- Navigate to the ALwrity project folder:
  ```
  cd /path/to/AI-Writer/Getting\ Started
  ```

### 2. Run the Installer
- Run:
  ```
  python3 setup.py install
  ```
- The script will check your system and install everything needed.
- If you see errors about Python or Rust, follow the on-screen instructions to install them, then re-run the script.

### 3. Start ALwrity
- Activate the virtual environment:
  ```
  source venv/bin/activate
  ```
- Start the app:
  ```
  streamlit run alwrity.py
  ```
- Or use the command:
  ```
  alwrity
  ```

---

## Troubleshooting
- **Python version error:**
  - Make sure you have Python 3.11.x installed and are using `python3`.
- **Rust not found:**
  - Install Rust with:
    ```
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
    ```
- **Other errors:**
  - Check the `install_errors.log` file in the folder for details.
  - Copy the error and [open an issue on GitHub](https://github.com/AJaySi/AI-Writer/issues).

---

## FAQ
- **Do I need to install anything else?**
  - No, `setup.py` will handle everything for you if prerequisites are met.
- **Can I run this on Windows?**
  - Use the Windows installer (`install_alwrity.bat`) instead.
- **Is it safe?**
  - Yes, the script only installs ALwrity and its dependencies.

---

## Need More Help?
- [Open an issue on GitHub](https://github.com/AJaySi/AI-Writer/issues)
- Join our support community

---
