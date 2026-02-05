from fastapi import APIRouter
from datetime import datetime
import psutil
import torch
import asyncio

from app.core.config import settings
from app.services.ml_service import MLService

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "service": "Eye Disease Detection API"
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics"""
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # ML model status
        ml_service = MLService()
        model_loaded = ml_service.is_model_loaded()
        
        # GPU status (if available)
        gpu_available = torch.cuda.is_available()
        gpu_memory = None
        if gpu_available:
            gpu_memory = {
                "allocated": torch.cuda.memory_allocated(),
                "cached": torch.cuda.memory_reserved(),
                "total": torch.cuda.get_device_properties(0).total_memory
            }
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.VERSION,
            "system": {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent
                },
                "disk": {
                    "total": disk.total,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                }
            },
            "ml_model": {
                "loaded": model_loaded,
                "model_path": settings.MODEL_PATH
            },
            "gpu": {
                "available": gpu_available,
                "memory": gpu_memory
            }
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


@router.get("/models/status")
async def model_status():
    """Check ML model loading status"""
    try:
        ml_service = MLService()
        
        return {
            "model_loaded": ml_service.is_model_loaded(),
            "model_path": settings.MODEL_PATH,
            "confidence_threshold": settings.MODEL_CONFIDENCE_THRESHOLD,
            "supported_formats": settings.ALLOWED_IMAGE_TYPES,
            "max_image_size": settings.MAX_IMAGE_SIZE
        }
        
    except Exception as e:
        return {
            "model_loaded": False,
            "error": str(e)
        }


@router.get("/readiness")
async def readiness_check():
    """Kubernetes readiness probe"""
    try:
        # Check if ML model is loaded
        ml_service = MLService()
        if not ml_service.is_model_loaded():
            return {"status": "not_ready", "reason": "ML model not loaded"}
        
        # Check database connection (simplified)
        # In production, you'd check actual DB connectivity
        
        return {"status": "ready"}
        
    except Exception as e:
        return {"status": "not_ready", "reason": str(e)}


@router.get("/liveness")
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}