#!/usr/bin/env python3
import subprocess
import sys
import time

def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(["docker", "info"], 
                              capture_output=True, 
                              text=True)
        if result.returncode != 0:
            print("❌ Docker is not running. Starting Docker...")
            # Try to start Docker (Linux)
            subprocess.run(["sudo", "systemctl", "start", "docker"])
            time.sleep(3)
    except FileNotFoundError:
        print("❌ Docker is not installed!")
        print("Install Docker first: https://docs.docker.com/get-docker/")
        sys.exit(1)

def main():
    print("💎 Starting Shiny Jar Business Suite")
    print("=" * 50)
    
    # Check Docker
    check_docker()
    
    # Build and start
    print("🔨 Building containers...")
    subprocess.run(["docker-compose", "build"])
    
    print("🚀 Starting services...")
    subprocess.run(["docker-compose", "up", "-d"])
    
    print("\n✅ Done! Services are starting...")
    print("\nOpen in browser:")
    print("   Frontend: http://localhost:8501")
    print("   Backend:  http://localhost:8000")
    print("\nTo view logs: docker-compose logs -f")
    print("To stop:      docker-compose down")

if __name__ == "__main__":
    main()