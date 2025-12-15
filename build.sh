#!/bin/bash
# Render.com build script - build.sh
# Optimized for memory usage

echo "Starting optimized build process..."

# Install dependencies with memory optimization
pip install --no-cache-dir -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Cleaning up build artifacts..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo "Build completed successfully!"