
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
