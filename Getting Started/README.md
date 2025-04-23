# ALwrity Installation Guide: Start Here!

Welcome to ALwrity! This guide will help you choose the best installation method for your needs, whether you're a non-technical user or a developer. Please read the options below and follow the recommended path for your system.

---

## Which Installation Method Should I Use?

### 1. **Docker (Recommended for Most Users, All Platforms)**
- **Best for:** Anyone who wants a hassle-free, one-command setup on Windows, Mac, or Linux.
- **Why choose Docker?**
  - No need to install Python, Rust, or system libraries manually.
  - Everything runs in a safe, isolated environment.
  - Consistent experience across all operating systems.
- **How to use:**
  - See [README_dockerfile.md](./README_dockerfile.md) for step-by-step instructions.

### 2. **Windows One-Click Installer (`install_alwrity.bat`)**
- **Best for:** Windows users who prefer a simple double-click installer.
- **Why choose this?**
  - Checks and installs all prerequisites for you (Python, Rust, Visual C++ Build Tools).
  - Minimal technical knowledge required.
- **How to use:**
  - See [README_install_bat.md](./README_install_bat.md) for detailed instructions.

### 3. **Manual Setup for Linux/macOS (`setup.py`)**
- **Best for:** Linux/macOS users who are comfortable with the terminal.
- **Why choose this?**
  - Gives you more control over the environment.
  - Useful if you want to customize or develop ALwrity.
- **How to use:**
  - See [README_setup_py.md](./README_setup_py.md) for a full walkthrough.

---

## Quick Decision Table
| Your System         | Easiest Method         | File/Guide to Use         |
|---------------------|-----------------------|--------------------------|
| Windows (any)       | Docker or install_alwrity.bat | README_dockerfile.md or README_install_bat.md |
| Mac                 | Docker                | README_dockerfile.md      |
| Linux               | Docker                | README_dockerfile.md      |
| Linux/macOS (dev)   | setup.py (manual)     | README_setup_py.md        |

---

## Still Unsure?
- If you are not sure, **Docker is the safest and easiest choice** for most users.
- If you run into any issues, check the troubleshooting sections in each guide or [open an issue on GitHub](https://github.com/AJaySi/AI-Writer/issues).

---

Happy writing!
