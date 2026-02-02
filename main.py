from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.moderation import moderation_router, limiter
from app.api.realty import realty_router
from app.api.auth import auth_router
from fastapi.responses import JSONResponse
from fastapi import Request
from loguru import logger
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.middleware.monitoring import PrometheusMiddleware
from app.monitoring.prometheus import metrics_router

app = FastAPI(title="Content Moderation API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # In production, replace with specific origins like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )


@app.get("/")
async def root():
    return {"message": "FastAPI with Prometheus Monitoring"}

app.include_router(moderation_router, prefix="/api/v1")
app.include_router(realty_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
 
app.include_router(metrics_router)
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)