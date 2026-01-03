# backend/test_server.py
import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Test server working", "port": os.getenv("PORT", "not set")}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)