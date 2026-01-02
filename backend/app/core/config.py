import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5433")
    DB_NAME = os.getenv("DB_NAME", "shinyjar_db")
    DB_USER = os.getenv("DB_USER", "shinyjar")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "shinyjar123")
    
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # App
    APP_NAME = os.getenv("APP_NAME", "Shiny Jar Business Suite")
    SECRET_KEY = os.getenv("SECRET_KEY", "Boku2003")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()