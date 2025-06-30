cd "Getting Started/Option_3_Docker_Install"
docker-compose up --build---

## Using ALwrity with Docker (Recommended for All Users)

### What is Docker?
Docker lets you run ALwrity in a safe, isolated environment on any computer (Windows, Mac, Linux) without worrying about Python or system setup. Think of it as a "ready-to-go" box for the app.

### Step 1: Install Docker
- Go to [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
- Download and install Docker Desktop for your operating system (Windows/Mac) or follow the Linux instructions.
- After installation, restart your computer if prompted.
- To check Docker is working, open a terminal and run:
  ```bash
  docker --version
  ```
  You should see a version number.

### Step 2: Build and Run ALwrity with Docker Compose (Recommended)
1. Open a terminal.
2. Navigate to the **Option_3_Docker_Install** folder:
   ```bash
   cd "Getting Started/Option_3_Docker_Install"
   ```
3. Build and start the app using Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Wait until you see a message like:
   ```
   Local URL: http://localhost:8501
   ```
5. Open your web browser and go to [http://localhost:8501](http://localhost:8501)
6. Follow the on-screen instructions to set up your API keys and start creating content!

### Stopping ALwrity
- To stop the app, press `Ctrl+C` in the terminal where Docker Compose is running.
- To remove the containers, run:
  ```bash
  docker-compose down
  ```

### Advanced: Manual Docker Build/Run (Optional)
If you prefer not to use Docker Compose, you can build and run manually:
```bash
cd /workspaces/AI-Writer
# Build the image
docker build -t alwrity -f "Getting Started/Option_3_Docker_Install/Dockerfile" .
# Run the container
docker run -p 8501:8501 alwrity
```

### Advanced: Saving Your Work
- By default, any files you create inside Docker are lost when the container stops.
- To save your work to your computer, use a volume:
  ```bash
  docker run -p 8501:8501 -v $(pwd)/alwrity_data:/app/your_data_folder alwrity
  ```

### Advanced: Publishing to Docker Hub
To build and push your image to Docker Hub:
```bash
docker build -t yourdockerhubusername/alwrity:latest -f "Getting Started/Option_3_Docker_Install/Dockerfile" .
docker push yourdockerhubusername/alwrity:latest
```

---