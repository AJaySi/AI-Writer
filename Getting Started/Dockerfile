# =====================================================================
# ALwrity Automated Dockerfile - Best Practices & Full Functionality
# =====================================================================
# This Dockerfile is designed for cache efficiency, security, and ease of use.
# It uses multi-stage builds for smaller images and leverages Docker layer caching.
# =====================================================================

# 1. Use official Python 3.11 image (builder stage)
FROM python:3.12

# 2. Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Install build dependencies first (for cache efficiency)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        git \
        curl \
        wget \
        libffi-dev \
        libssl-dev \
        rustc \
        cargo \
    && rm -rf /var/lib/apt/lists/*

# 4. Set work directory
WORKDIR /app

# 5. Copy only requirements.txt first (for better caching)
COPY ../requirements.txt ./

# 6. Install Python dependencies in builder
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# === Start runtime stage ===
FROM python:3.11-slim AS runtime

# 7. Copy app source code and requirements.txt to runtime image
COPY ../requirements.txt ./
COPY ../alwrity.py /app/
COPY ../lib /app/lib

# 8. Install Python dependencies in runtime as root
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 9. Create a non-root user for security
RUN useradd -m alwrityuser

# 10. Set environment variable for Streamlit (optional: disables telemetry)
ENV STREAMLIT_TELEMETRY=0

# 11. Set work directory
WORKDIR /app

# 12. Create logs directory and set permissions
RUN mkdir -p /app/logs && chown -R alwrityuser:alwrityuser /app/logs

# 13. Expose Streamlit's default port
EXPOSE 8501

# 14. Switch to non-root user
USER alwrityuser

# 15. Add user local bin to PATH
ENV PATH="/home/alwrityuser/.local/bin:$PATH"

# 16. Default command: run ALwrity with Streamlit
CMD ["streamlit", "run", "alwrity.py", "--server.port=8501", "--server.address=0.0.0.0"]

# =====================================================================
# END OF DOCKERFILE
# =====================================================================
