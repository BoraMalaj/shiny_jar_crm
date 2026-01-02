#!/bin/bash

cd ~/shiny_jar_suite/backend

# Set Python path
export PYTHONPATH=/home/beni/shiny_jar_suite/backend:$PYTHONPATH

# Activate virtual environment
source venv/bin/activate

# Run with correct path
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload