import os

class Settings:
    # Get DATABASE_URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Debug: Print the DATABASE_URL (for troubleshooting, remove in production)
    if not DATABASE_URL:
        print("WARNING: DATABASE_URL is not set!")
    else:
        print(f"DATABASE_URL found: {DATABASE_URL[:20]}...")  # Print first 20 chars
    
    # Convert postgres:// to postgresql:// for SQLAlchemy (Railway uses postgres://)
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # App Settings
    APP_NAME = os.getenv("APP_NAME", "Shiny Jar Business Suite")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()