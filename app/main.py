"""FastAPI application for Realty API."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.realty import realty_router
from app.middleware.monitoring import PrometheusMiddleware
from app.monitoring.prometheus import metrics_router
import os
import logging

logging.basicConfig(level=logging.INFO)

logging.info("ENV=%s", os.getenv("ENV"))
logging.info("DB_HOST=%s", os.getenv("DB_HOST"))
logging.info("DB_PORT=%s", os.getenv("DB_PORT"))
logging.info("DB_USER=%s", os.getenv("DB_USER"))
logging.info("DB_NAME=%s", os.getenv("DB_NAME"))

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Realty API",
    description="API for managing property listings and contacts",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred"
        }
    )


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Realty API"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "Realty API",
        "version": "1.0.0"
    }


# Include routers
app.include_router(realty_router, prefix="/api/v1")
app.include_router(metrics_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)