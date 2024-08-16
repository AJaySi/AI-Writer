import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """
    Configuration settings for the FastAPI application.
    These settings are loaded from environment variables.
    """
    app_name: str = Field(..., env="APP_NAME")
    environment: str = Field(..., env="ENVIRONMENT")
    database_url: str = Field(..., env="DATABASE_URL")
    api_key: str = Field(..., env="API_KEY")
    debug: bool = Field(False, env="DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    """
    Retrieve the settings instance.
    This function can be used as a dependency in FastAPI routes.
    """
    return Settings()

