#!/usr/bin/env python3
import subprocess
import sys
import os

def run_command(cmd, description):
    print(f"\n🔧 {description}...")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed: {cmd}")
        sys.exit(1)
    print("✅ Done")

def main():
    print("🚀 Setting up Shiny Jar Business Suite Development Environment")
    
    # Check Python version
    run_command("python --version", "Checking Python version")
    
    # Create virtual environment
    if not os.path.exists("venv"):
        run_command("python -m venv venv", "Creating virtual environment")
    
    # Activate venv and install requirements
    print("\n📦 Installing dependencies...")
    
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate && "
    else:
        activate_cmd = "source venv/bin/activate && "
    
    run_command(
        f"{activate_cmd} pip install --upgrade pip",
        "Upgrading pip"
    )
    
    run_command(
        f"{activate_cmd} pip install -r requirements.txt",
        "Installing Python packages"
    )
    
    # Setup database
    print("\n🗄️  Setting up database...")
    run_command(
        "docker run --name shinyjar-db -p 5435:5432 -e POSTGRES_PASSWORD=postgres -d postgres:15",
        "Starting PostgreSQL container"
    )
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Activate virtual environment:")
    print("   source venv/bin/activate  # Linux/Mac")
    print("   venv\\Scripts\\activate    # Windows")
    print("\n2. Start backend server:")
    print("   cd backend && python -m app.main")
    print("\n3. Start frontend (in new terminal):")
    print("   cd frontend && streamlit run app.py")
    print("\n4. Open browser:")
    print("   Backend API: http://localhost:8000")
    print("   Frontend: http://localhost:8501")
    print("   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()