import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_db():
    """
    Dependency that provides a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_settings():
    """
    Dependency that provides application settings.
    """
    class Settings:
        app_name: str = "Alwrity"
        admin_email: str = os.getenv("ADMIN_EMAIL")
        items_per_user: int = 50

    return Settings()

# Example usage in a FastAPI route
# from fastapi import Depends, FastAPI
# from .dependencies import get_db, get_settings

# app = FastAPI()

# @app.get("/items/")
# def read_items(db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
#     return {"app_name": settings.app_name, "items": db.query(Item).all()}

