"""
FastAPI backend for eye infection detection API
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import aiofiles
import os
from typing import Optional
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.preprocessing import preprocess_image, validate_image_format
from utils.inference import EyeDiseaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Eye Infection Detection API",
    description="API for preliminary eye infection detection using non-microscopic eye photographs",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
model: Optional[EyeDiseaseModel] = None

# Constants
UPLOAD_DIR = "uploads"
MODEL_PATH = "backend/model/eye_disease_model.keras"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.on_event("startup")
async def startup_event():
    """Load model on application startup."""
    global model
    
    print("Starting up Eye Infection Detection API...")
    
    # Check if model file exists
    if os.path.exists(MODEL_PATH):
        print(f"Loading model from {MODEL_PATH}...")
        model = EyeDiseaseModel(MODEL_PATH)
    else:
        print(f"Warning: Model file not found at {MODEL_PATH}")
        print("API will return error messages. Please train and save the model first.")
        print("Use the training notebook in /training/ directory.")
        model = None
    
    print("API startup complete!")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Eye Infection Detection API",
        "version": "1.0.0",
        "status": "ready" if model else "model_not_loaded",
        "endpoints": {
            "predict": "/predict",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict eye disease from uploaded image.
    
    Args:
        file: Uploaded image file (JPEG/PNG)
    
    Returns:
        JSON response with predicted class and confidence score
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train and save the model first."
        )
    
    # Validate file type
    if not validate_image_format(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only JPEG and PNG images are supported."
        )
    
    try:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        temp_filename = f"{file.filename}"
        temp_path = os.path.join(UPLOAD_DIR, temp_filename)
        
        # Save uploaded file
        async with aiofiles.open(temp_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Preprocess image
        preprocessed_image = preprocess_image(temp_path, target_size=(224, 224))
        
        # Run prediction
        result = model.predict(preprocessed_image)
        
        # Clean up temporary file
        try:
            os.remove(temp_path)
        except:
            pass
        
        return JSONResponse(
            content={
                "success": True,
                "predicted_class": result['predicted_class'],
                "confidence_score": round(result['confidence_score'], 4)
            }
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/classes")
async def get_classes():
    """Get list of supported disease classes."""
    return {
        "classes": model.class_names if model else [
            'Normal',
            'Conjunctivitis',
            'Cataract',
            'Glaucoma'
        ]
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
