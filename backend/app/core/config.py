import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DB_HOST = os.getenv("DB_HOST")                # os.getenv("DB_HOST", DB_HOST)
    DB_PORT = os.getenv("DB_PORT")                # os.getenv("DB_PORT", DB_PORT)
    DB_NAME = os.getenv("DB_NAME")                # os.getenv("DB_NAME", DB_NAME)
    DB_USER = os.getenv("DB_USER")                # os.getenv("DB_USER", DB_USER)
    DB_PASSWORD = os.getenv("DB_PASSWORD")        # os.getenv("DB_PASSWORD", DB_PASSWORD)
    
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # App
    APP_NAME = os.getenv("APP_NAME", "Shiny Jar Business Suite")
    SECRET_KEY = os.getenv("SECRET_KEY", "SECRET_KEY")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()