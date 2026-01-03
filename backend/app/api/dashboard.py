# backend/app/api/dashboard.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/dashboard")
async def get_dashboard(token: str = Depends(oauth2_scheme)):
    # Verify token and return dashboard data
    return {"dashboard": "data"}