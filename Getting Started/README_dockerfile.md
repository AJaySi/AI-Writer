---

## Using ALwrity with Docker (Recommended for All Users)

### What is Docker?
Docker lets you run ALwrity in a safe, isolated environment on any computer (Windows, Mac, Linux) without worrying about Python or system setup. Think of it as a "ready-to-go" box for the app.

### Step 1: Install Docker
- Go to [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
- Download and install Docker Desktop for your operating system (Windows/Mac) or follow the Linux instructions.
- After installation, restart your computer if prompted.
- To check Docker is working, open a terminal and run:
  ```
  docker --version
  ```
  You should see a version number.

### Step 2: Build the ALwrity Docker Image (No Manual Download Needed!)
1. Open a terminal.
2. Navigate to the `Getting Started` folder in your workspace:
   ```
   cd /workspaces/AI-Writer/Getting\ Started
   ```
3. Build the Docker image (this will automatically download the latest ALwrity code from GitHub):
   ```
   docker build -t alwrity .
   ```
   > **Note:** You do NOT need to manually download or clone the project. The Dockerfile will do this for you!

### Step 3: Run ALwrity in Docker
1. Start the app with this command:
   ```
   docker run -p 8501:8501 alwrity
   ```
2. Wait until you see a message like:
   ```
   Local URL: http://localhost:8501
   ```
3. Open your web browser and go to [http://localhost:8501](http://localhost:8501)
4. Follow the on-screen instructions to set up your API keys and start creating content!

### Stopping ALwrity
- To stop the app, go back to the terminal and press `Ctrl+C`.

### Advanced: Saving Your Work
- By default, any files you create inside Docker are lost when the container stops.
- To save your work to your computer, run:
  ```
  docker run -p 8501:8501 -v $(pwd)/alwrity_data:/app/your_data_folder alwrity
  ```
  Replace `your_data_folder` with the folder ALwrity uses for output (see documentation).

### Troubleshooting
- If you see errors about missing ports or permissions, make sure Docker Desktop is running.
- If you get a 'permission denied' error on Linux, try running with `sudo`:
  ```
  sudo docker run -p 8501:8501 alwrity
  ```
- For other issues, check the Troubleshooting section below or open an issue on GitHub.

---

## Need More Help?
- Visit the [official Docker documentation](https://docs.docker.com/get-started/)
- Open an issue on our GitHub page
- Join our support community

---