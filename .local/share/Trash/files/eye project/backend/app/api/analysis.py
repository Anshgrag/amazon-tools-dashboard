from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid
import json

from app.core.database import get_db
from app.core.security import get_current_user, validate_image_file
from app.core.config import settings
from app.schemas.analysis import AnalysisResponse, AnalysisRequest
from app.models.auth import User
from app.models.analysis import EyeScan
from app.core.exceptions import ValidationError, ImageProcessingError, ModelError
from app.services.ml_service import MLService
from app.services.image_service import ImageService

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_eye_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze uploaded eye image for disease detection
    """
    # Validate file
    if not file.content_type or not file.content_type.startswith('image/'):
        raise ValidationError("File must be an image")
    
    # Read file content
    file_content = await file.read()
    
    # Validate image
    if not validate_image_file(file_content, file.content_type):
        raise ValidationError("Invalid image file or size too large")
    
    # Generate scan ID
    scan_id = str(uuid.uuid4())
    
    # Create scan record
    scan = await EyeScan.create(
        db=db,
        user_id=current_user.id,
        scan_id=scan_id,
        image_data=file_content,
        image_type=file.content_type,
        status="processing"
    )
    
    # Process image in background
    background_tasks.add_task(
        process_eye_scan,
        scan_id=scan_id,
        file_content=file_content,
        file_type=file.content_type
    )
    
    return AnalysisResponse(
        scan_id=scan_id,
        status="processing",
        message="Image uploaded successfully. Processing started.",
        timestamp=datetime.utcnow(),
        disclaimer=settings.MEDICAL_DISCLAIMER
    )


@router.get("/results/{scan_id}", response_model=AnalysisResponse)
async def get_analysis_results(
    scan_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get analysis results for a specific scan
    """
    # Get scan record
    scan = await EyeScan.get_by_scan_id(db, scan_id)
    if not scan:
        raise ValidationError("Scan not found")
    
    # Verify ownership
    if scan.user_id != current_user.id:
        raise ValidationError("Access denied")
    
    # Return results
    if scan.status == "completed":
        return AnalysisResponse(
            scan_id=scan_id,
            status="completed",
            prediction=scan.prediction,
            confidence=scan.confidence,
            visual_features=scan.visual_features,
            explanation=scan.explanation,
            timestamp=scan.created_at,
            disclaimer=settings.MEDICAL_DISCLAIMER
        )
    elif scan.status == "failed":
        return AnalysisResponse(
            scan_id=scan_id,
            status="failed",
            message=scan.error_message,
            timestamp=scan.created_at,
            disclaimer=settings.MEDICAL_DISCLAIMER
        )
    else:
        return AnalysisResponse(
            scan_id=scan_id,
            status="processing",
            message="Analysis in progress...",
            timestamp=scan.created_at,
            disclaimer=settings.MEDICAL_DISCLAIMER
        )


@router.get("/history")
async def get_scan_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """
    Get user's scan history
    """
    scans = await EyeScan.get_user_scans(
        db=db,
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )
    
    return {
        "scans": [
            {
                "scan_id": scan.scan_id,
                "status": scan.status,
                "prediction": scan.prediction,
                "confidence": scan.confidence,
                "created_at": scan.created_at
            }
            for scan in scans
        ],
        "total": len(scans),
        "limit": limit,
        "offset": offset
    }


async def process_eye_scan(
    scan_id: str,
    file_content: bytes,
    file_type: str
):
    """
    Background task to process eye scan
    """
    from app.core.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        try:
            # Get scan record
            scan = await EyeScan.get_by_scan_id(db, scan_id)
            if not scan:
                return
            
            # Preprocess image
            image_service = ImageService()
            processed_image = await image_service.preprocess_eye_image(file_content)
            
            # Run ML inference
            ml_service = MLService()
            result = await ml_service.predict(processed_image)
            
            # Update scan with results
            await scan.update_results(
                db=db,
                prediction=result["prediction"],
                confidence=result["confidence"],
                visual_features=result["visual_features"],
                explanation=result["explanation"],
                status="completed"
            )
            
        except Exception as e:
            # Update scan with error
            await scan.update_error(
                db=db,
                error_message=str(e),
                status="failed"
            )