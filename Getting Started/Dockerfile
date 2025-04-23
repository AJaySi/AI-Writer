# =====================================================================
# ALwrity Automated Dockerfile - Zero Manual Steps for End Users
# =====================================================================
# This Dockerfile will automatically:
# 1. Use Python 3.11
# 2. Install all system dependencies (build tools, Rust, etc.)
# 3. Clone the latest ALwrity code from GitHub
# 4. Install Python dependencies
# 5. Set up a non-root user
# 6. Expose Streamlit port and run the app
# =====================================================================

# 1. Use official Python 3.11 image
FROM python:3.11-slim as base

# 2. Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        git \
        curl \
        wget \
        nano \
        libffi-dev \
        libssl-dev \
        rustc \
        cargo \
    && rm -rf /var/lib/apt/lists/*

# 4. Set work directory
WORKDIR /app

# 5. Clone the latest ALwrity code from GitHub
RUN git clone https://github.com/AJaySi/AI-Writer.git .

# 6. Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Create a non-root user for security
RUN useradd -m alwrityuser
USER alwrityuser

# 8. Expose Streamlit's default port
EXPOSE 8501

# 9. Set environment variable for Streamlit (optional: disables telemetry)
ENV STREAMLIT_TELEMETRY=0

# 10. Default command: run ALwrity with Streamlit
CMD ["streamlit", "run", "alwrity.py", "--server.port=8501", "--server.address=0.0.0.0"]

# =====================================================================
# END OF DOCKERFILE
# =====================================================================
