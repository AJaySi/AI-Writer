# =====================================================================
# ALwrity Automated Dockerfile - Best Practices & Full Functionality
# =====================================================================
# This Dockerfile is designed for cache efficiency, security, and ease of use.
# It uses multi-stage builds for smaller images and leverages Docker layer caching.
# =====================================================================

# 1. Use official Python 3.12 image (builder stage)
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
FROM python:3.12-slim AS runtime

# 7. Install build tools needed for wordcloud
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*

# 8. Set work directory
WORKDIR /app

# 9. Copy app source code, requirements, and .env to runtime image
COPY ../requirements.txt ./
COPY ../alwrity.py /app/
COPY ../lib /app/lib

# Create the .env file with default values
RUN echo "# Default environment variables for ALwrity\n" > /app/.env

# 10. Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 11. Create a non-root user for security
RUN useradd -m alwrityuser

# 12. Change ownership of /app and .env to the non-root user
RUN chown -R alwrityuser:alwrityuser /app

# 13. Set environment variable for Streamlit (optional: disables telemetry)
ENV STREAMLIT_TELEMETRY=0

# 14. Expose Streamlit's default port
EXPOSE 8501

# 15. Switch to non-root user
USER alwrityuser

# 16. Add user local bin to PATH
ENV PATH="/home/alwrityuser/.local/bin:$PATH"

# 17. Default command: run ALwrity with Streamlit
CMD ["streamlit", "run", "alwrity.py", "--server.port=8501", "--server.address=0.0.0.0"]

# =====================================================================
# END OF DOCKERFILE
# =====================================================================
