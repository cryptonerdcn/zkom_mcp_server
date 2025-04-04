"""
Main application entry point
"""
import os
import logging
import logging.config
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    API_PREFIX,
    LOGGING_CONFIG
)
from app.api.routes import router as api_router

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=API_PREFIX)


@app.middleware("http")
async def add_request_id_header(request: Request, call_next):
    """
    Add a request ID header to responses if not present in the request
    """
    response = await call_next(request)
    if "X-Request-ID" not in response.headers and "x-request-id" in request.headers:
        response.headers["X-Request-ID"] = request.headers["x-request-id"]
    return response


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok", "service": API_TITLE, "version": API_VERSION}


@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "service": API_TITLE,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "docs_url": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting {API_TITLE} v{API_VERSION} on {host}:{port}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    ) 