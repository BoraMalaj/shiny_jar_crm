# backend/app/api/debug.py
@router.get("/debug/token")
async def debug_token(token: str = Depends(oauth2_scheme)):
    return {
        "token_valid": True,
        "token_preview": token[:20] + "..." if token else "None"
    }