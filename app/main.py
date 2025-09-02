from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.core.config import settings
from app.core.database import engine, Base
from app.core.redis_client import redis_client
from app.api.v1 import auth, transfers, fraud
from app.core.middleware import setup_middleware
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events"""
    # Startup
    logger.info("Starting fraud detection transfer system...")
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Test Redis connection
    try:
        await redis_client.ping()
        logger.info("Redis connection successful")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await redis_client.close()


app = FastAPI(
    title="Fraud Detection Transfer System",
    description="A sophisticated fraud detection and money transfer system",
    version="0.1.0",
    lifespan=lifespan
)

# Setup middleware
setup_middleware(app)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["authentication"])
app.include_router(transfers.router, prefix="/api/v1", tags=["transfers"])
app.include_router(fraud.router, prefix="/api/v1", tags=["fraud-detection"])


@app.get("/")
async def root():
    return {"message": "Fraud Detection Transfer System API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check Redis
        await redis_client.ping()
        redis_status = "healthy"
    except Exception:
        redis_status = "unhealthy"
    
    return {
        "status": "healthy",
        "redis": redis_status,
        "database": "healthy"
    }