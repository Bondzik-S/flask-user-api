"""Configuration module for Flask User API."""

import os
from dotenv import load_dotenv

load_dotenv()


def get_database_host() -> str:
    """Get database host based on environment.
    
    If running in Docker (container environment), use 'db' as host.
    Otherwise, use 'localhost' for local development.
    
    Returns:
        str: Database host name
    """
    # Check if running in Docker container
    if os.path.exists('/.dockerenv'):
        return os.getenv("POSTGRES_HOST", "db")
    return os.getenv("POSTGRES_HOST", "localhost")


class Config:
    """Base configuration class for Flask User API."""

    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = get_database_host()
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """Configuration for testing environment."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
