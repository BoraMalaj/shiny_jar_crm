from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Check if DATABASE_URL is set
if not settings.DATABASE_URL:
    # List all environment variables (masked) for debugging
    import os
    env_vars = {k: "****" if "PASS" in k.upper() or "SECRET" in k.upper() or "KEY" in k.upper() else v 
                for k, v in os.environ.items()}
    
    error_msg = f"""
    DATABASE_URL is not set! 
    
    Available environment variables: {env_vars}
    
    Possible fixes:
    1. Add PostgreSQL database to the SAME project in Railway
    2. Manually set DATABASE_URL variable with connection string
    3. Set individual DB_* variables (DB_HOST, DB_USER, etc.)
    
    Current settings.DATABASE_URL value: {settings.DATABASE_URL}
    """
    raise ValueError(error_msg)

print(f"Creating engine with DATABASE_URL (masked): {settings.DATABASE_URL[:50]}...")

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()