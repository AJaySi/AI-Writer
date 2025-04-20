# install Python base image with build tools
# We need build-essential and python3-dev for compiling some dependencies to avoid errs hopefully ;0
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for some Python packages & rust
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential python3-dev curl && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Rust's directory to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy the requirements file first 
COPY requirements.txt ./

# Install Python dependencies
# --no-cache-dir used ti prevent pip from caching packages reducing the image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose a port 
EXPOSE 8501

# run the Streamlit application
CMD ["streamlit", "run", "alwrity.py"]

# Note: This Dockerfile assumes you have the project code 
# So make sure you run `git clone https://github.com/AJaySi/AI-Writer` 
# in the directory where you build the Docker image.
