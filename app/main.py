import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import router as app_router

# Load environment variables from .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Include the routes from app/routes.py
app.include_router(app_router)

# Add any necessary middleware or configurations here

# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

