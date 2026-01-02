#!/usr/bin/env python3
import subprocess
import sys
import os

def run_backend():
    """Start the backend server"""
    print("🚀 Starting Shiny Jar Backend...")
    os.chdir("backend")
    sys.path.insert(0, os.getcwd())
    from app.main import app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

def run_frontend():
    """Start the frontend server"""
    print("🎨 Starting Shiny Jar Frontend...")
    os.chdir("frontend")
    import subprocess
    subprocess.run(["streamlit", "run", "app.py", "--server.port=8501"])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "backend":
            run_backend()
        elif sys.argv[1] == "frontend":
            run_frontend()
        elif sys.argv[1] == "all":
            # This would need multiprocessing, but for now:
            print("Use docker-compose up to run both")
    else:
        print("Usage: python run.py [backend|frontend|all]")
        print("Or use: docker-compose up")