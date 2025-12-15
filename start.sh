#!/bin/bash
# Render.com startup script
# Uses optimized gunicorn configuration

echo "Starting NRC System with optimized configuration..."

# Set memory limits
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Start gunicorn with optimized settings
exec gunicorn --config gunicorn.conf.py nrc_system.wsgi:application