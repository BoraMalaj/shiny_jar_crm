import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Convert postgres:// to postgresql:// for SQLAlchemy
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # App Settings
    APP_NAME = os.getenv("APP_NAME", "Shiny Jar Business Suite")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
