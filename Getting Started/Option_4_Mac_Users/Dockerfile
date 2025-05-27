# Use Python 3.8 slim image optimized for M1/M2 Macs
FROM --platform=linux/arm64 python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/AJaySi/AI-Writer.git .

# Install Python dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "alwrity.py"]