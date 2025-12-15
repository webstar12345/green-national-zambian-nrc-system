# Gunicorn configuration for Render.com
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