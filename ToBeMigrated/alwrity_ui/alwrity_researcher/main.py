import streamlit as st
import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

# Import the dashboard module
from dashboard import main

# Run the dashboard
if __name__ == "__main__":
    main()