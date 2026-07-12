#!/bin/bash

# Initialize database
python -m app.db.init_db

# Seed database with initial users
python -m app.db.seed_db

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8000
