from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from backend.app.core.config import settings
from backend.app.core.database import engine, Base
from backend.app.api.v1 import auth, expenses, customers, analytics

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Shiny Jar Business Suite...")
    Base.metadata.create_all(bind=engine)
    yield
    print("🛑 Shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(expenses.router, prefix="/api/v1", tags=["expenses"])
app.include_router(customers.router, prefix="/api/v1", tags=["customers"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Shiny Jar Business Suite",
        "version": settings.VERSION,
        "docs": "/docs",
        "instagram": "https://instagram.com/shiny_jar"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)