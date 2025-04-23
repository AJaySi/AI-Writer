# =====================================================================
# ALwrity Automated Dockerfile - Best Practices & Full Functionality
# =====================================================================
# This Dockerfile is designed for cache efficiency, security, and ease of use.
# It uses multi-stage builds for smaller images and leverages Docker layer caching.
# =====================================================================

# 1. Use official Python 3.11 image (builder stage)
FROM python:3.11-slim AS builder

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
COPY ../../requirements.txt ./

# 6. Install Python dependencies in builder
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Clone the latest ALwrity code from GitHub (after dependencies for cache efficiency)
RUN git clone https://github.com/AJaySi/AI-Writer.git .

# 8. Copy only necessary files to the final image (runtime stage)
FROM python:3.11-slim AS runtime

# 9. Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 10. Create a non-root user for security
RUN useradd -m alwrityuser
USER alwrityuser

# 11. Set work directory
WORKDIR /app

# 12. Copy installed packages and app from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

# 13. Expose Streamlit's default port
EXPOSE 8501

# 14. Set environment variable for Streamlit (optional: disables telemetry)
ENV STREAMLIT_TELEMETRY=0

# 15. Default command: run ALwrity with Streamlit
CMD ["streamlit", "run", "alwrity.py", "--server.port=8501", "--server.address=0.0.0.0"]

# =====================================================================
# END OF DOCKERFILE
# =====================================================================
