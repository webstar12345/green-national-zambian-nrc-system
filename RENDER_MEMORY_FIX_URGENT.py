#!/usr/bin/env python3
"""
Emergency Render.com Memory and Performance Fix
Addresses worker timeouts and memory issues
"""

def create_render_fixes():
    """Create files to fix Render.com memory and performance issues"""
    
    # 1. Create optimized gunicorn configuration
    gunicorn_config = """# Gunicorn configuration for Render.com
# Optimized for memory usage and performance

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:10000"
backlog = 2048

# Worker processes
workers = 1  # Reduced from default to save memory
worker_class = "sync"
worker_connections = 1000
timeout = 120  # Increased timeout to prevent worker kills
keepalive = 2

# Memory management
max_requests = 1000  # Restart workers after 1000 requests to prevent memory leaks
max_requests_jitter = 50
preload_app = True  # Preload app to save memory

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "nrc_system"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
"""
    
    with open('gunicorn.conf.py', 'w') as f:
        f.write(gunicorn_config)
    
    # 2. Create memory-optimized Django settings
    memory_settings = """
# Memory optimization settings for production
# Add these to your nrc_system/settings.py

import os

# Database connection pooling to reduce memory usage
DATABASES['default']['CONN_MAX_AGE'] = 60  # Reuse connections for 60 seconds

# Cache configuration to reduce database queries
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'nrc-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,  # Limit cache size
        }
    }
}

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

# Email backend optimization
if not DEBUG:
    # Use console backend in production if SMTP fails to reduce memory usage
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_TIMEOUT = 30  # Timeout for email sending

# Static files optimization
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging configuration to prevent log buildup
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
"""
    
    with open('MEMORY_OPTIMIZATION_SETTINGS.py', 'w') as f:
        f.write(memory_settings)
    
    # 3. Create build script for Render.com
    build_script = """#!/bin/bash
# Render.com build script - build.sh
# Optimized for memory usage

echo "🚀 Starting optimized build process..."

# Install dependencies with memory optimization
pip install --no-cache-dir -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

echo "🧹 Cleaning up build artifacts..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo "✅ Build completed successfully!"
"""
    
    with open('build.sh', 'w') as f:
        f.write(build_script)
    
    # 4. Create startup script
    startup_script = """#!/bin/bash
# Render.com startup script
# Uses optimized gunicorn configuration

echo "🚀 Starting NRC System with optimized configuration..."

# Set memory limits
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Start gunicorn with optimized settings
exec gunicorn --config gunicorn.conf.py nrc_system.wsgi:application
"""
    
    with open('start.sh', 'w') as f:
        f.write(startup_script)
    
    print("✅ Render.com optimization files created!")
    print()
    print("📋 Files created:")
    print("- gunicorn.conf.py: Optimized server configuration")
    print("- MEMORY_OPTIMIZATION_SETTINGS.py: Django memory settings")
    print("- build.sh: Optimized build script")
    print("- start.sh: Optimized startup script")

def create_render_environment_vars():
    """Show required Render.com environment variables"""
    print()
    print("🌐 RENDER.COM ENVIRONMENT VARIABLES")
    print("=" * 45)
    print()
    print("📋 Required variables for memory optimization:")
    print()
    print("# Python settings")
    print("PYTHONUNBUFFERED=1")
    print("PYTHONDONTWRITEBYTECODE=1")
    print()
    print("# Django settings")
    print("DEBUG=False")
    print("DJANGO_SETTINGS_MODULE=nrc_system.settings")
    print()
    print("# Email settings (your new secure password)")
    print("EMAIL_HOST_USER=simoongalaurent427@gmail.com")
    print("EMAIL_HOST_PASSWORD=uroaoegylbpusjfy")
    print("EMAIL_HOST=smtp.gmail.com")
    print("EMAIL_PORT=587")
    print("EMAIL_USE_TLS=True")
    print("DEFAULT_FROM_EMAIL=simoongalaurent427@gmail.com")
    print()
    print("# Memory optimization")
    print("WEB_CONCURRENCY=1")
    print("GUNICORN_CMD_ARGS=--timeout 120 --max-requests 1000")

def show_render_service_settings():
    """Show Render.com service configuration"""
    print()
    print("⚙️ RENDER.COM SERVICE SETTINGS")
    print("=" * 35)
    print()
    print("📋 Update these in your Render.com service:")
    print()
    print("Build Command:")
    print("./build.sh")
    print()
    print("Start Command:")
    print("./start.sh")
    print()
    print("Instance Type:")
    print("Starter (512 MB RAM) - Upgrade if needed")
    print()
    print("Auto-Deploy:")
    print("Yes (from main branch)")

def main():
    """Main function"""
    print("🚨 RENDER.COM MEMORY & PERFORMANCE FIX")
    print("=" * 45)
    print()
    print("🔍 ISSUES DETECTED FROM LOGS:")
    print("- WORKER TIMEOUT: Workers being killed")
    print("- OUT OF MEMORY: Workers running out of RAM")
    print("- SIGKILL: System forcibly killing processes")
    print("- Constant restarts: Application instability")
    print()
    print("💡 This explains why OTP emails aren't working!")
    print("   The app crashes before it can send emails.")
    print()
    
    while True:
        print("Choose an option:")
        print("1. 🛠️ Create optimization files")
        print("2. 🌐 Show environment variables")
        print("3. ⚙️ Show service settings")
        print("4. 📋 Show complete fix steps")
        print("5. 🚪 Exit")
        print()
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            create_render_fixes()
        elif choice == '2':
            create_render_environment_vars()
        elif choice == '3':
            show_render_service_settings()
        elif choice == '4':
            print("📋 COMPLETE FIX STEPS:")
            print("=" * 25)
            print("1. Run option 1 to create optimization files")
            print("2. Push all files to GitHub")
            print("3. Update Render.com environment variables (option 2)")
            print("4. Update Render.com service settings (option 3)")
            print("5. Wait for deployment")
            print("6. Test OTP emails")
        elif choice == '5':
            break
        else:
            print("❌ Invalid choice!")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()