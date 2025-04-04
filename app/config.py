"""
Application configuration
"""
import os
import logging
from typing import Dict, Any

# Server configuration
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

# API configuration
API_PREFIX = "/api"
API_TITLE = "ZKOM MCP Server"
API_DESCRIPTION = "Cryptocurrency price API using Model Context Protocol"
API_VERSION = "1.0.0"

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "app": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "uvicorn": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
} 