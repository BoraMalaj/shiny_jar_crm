from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

print(f"Database URL from settings: {settings.DATABASE_URL}")

# Add validation
if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables!")

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()