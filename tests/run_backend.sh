#!/bin/bash

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run from project root
cd ~/shiny_jar_suite
python -m backend.app.main