import os
from typing import Optional

class Settings:
    # Try multiple possible environment variable names
    DATABASE_URL: Optional[str] = None
    
    # Common environment variable names for database URL
    possible_db_urls = [
        "DATABASE_URL",
        "POSTGRES_URL",
        "POSTGRESQL_URL", 
        "RAILWAY_DATABASE_URL"
    ]
    
    for var_name in possible_db_urls:
        db_url = os.getenv(var_name)
        if db_url:
            DATABASE_URL = db_url
            print(f"Found database URL from {var_name}")
            break
    
    # If still not found, try constructing from individual parts
    if not DATABASE_URL:
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_NAME = os.getenv("DB_NAME")
        
        if all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
            DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            print("Constructed DATABASE_URL from individual parts")
    
    # Convert postgres:// to postgresql:// for SQLAlchemy
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        print("Converted postgres:// to postgresql://")
    
    # Debug output
    if DATABASE_URL:
        # Mask password in logs for security
        masked_url = DATABASE_URL
        if "@" in DATABASE_URL:
            parts = DATABASE_URL.split("@")
            auth_part = parts[0]
            if ":" in auth_part:
                user_pass = auth_part.split(":")
                if len(user_pass) > 1:
                    masked_url = f"{user_pass[0]}:****@{parts[1]}"
        print(f"Final DATABASE_URL: {masked_url}")
    else:
        print("ERROR: No DATABASE_URL found!")
        print("Available environment variables:", dict(os.environ))
    
    # App Settings
    APP_NAME = os.getenv("APP_NAME", "Shiny Jar Business Suite")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()