#!/bin/bash

echo "🔧 Fixing Shiny Jar Setup..."

# Go to project root
cd ~/shiny_jar_suite

# Create backend requirements if missing
if [ ! -f "backend/requirements.txt" ]; then
    echo "📝 Creating backend/requirements.txt..."
    cat > backend/requirements.txt << 'BACKEND_REQ'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
requests==2.31.0
BACKEND_REQ
fi

# Create frontend requirements if missing
if [ ! -f "frontend/requirements.txt" ]; then
    echo "📝 Creating frontend/requirements.txt..."
    cat > frontend/requirements.txt << 'FRONTEND_REQ'
streamlit==1.28.1
plotly==5.18.0
pandas==2.1.3
numpy==1.26.2
requests==2.31.0
FRONTEND_REQ
fi

# Create backend Dockerfile if missing
if [ ! -f "backend/Dockerfile" ]; then
    echo "📝 Creating backend/Dockerfile..."
    cat > backend/Dockerfile << 'BACKEND_DOCKERFILE'
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV DOCKER_ENV=true
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
BACKEND_DOCKERFILE
fi

# Create frontend Dockerfile if missing
if [ ! -f "frontend/Dockerfile" ]; then
    echo "📝 Creating frontend/Dockerfile..."
    cat > frontend/Dockerfile << 'FRONTEND_DOCKERFILE'
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
FRONTEND_DOCKERFILE
fi

echo "✅ Files created!"
echo ""
echo "📁 Verifying structure:"
ls -la backend/requirements.txt backend/Dockerfile frontend/requirements.txt frontend/Dockerfile

echo ""
echo "🚀 Now run: docker-compose up --build"
