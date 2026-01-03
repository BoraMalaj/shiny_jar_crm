# backend/test.py
import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "PORT": os.getenv("PORT", "NOT SET")}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting server on port {port}")
    print(f"📡 Host: 0.0.0.0")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")