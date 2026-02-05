# Quick Start Guide

## For Developers

### 1. Clone and Setup (2 minutes)

```bash
cd EYE
bash setup.sh
```

### 2. Train Model (15-30 minutes on Colab)

- Open `training/eye_detection_training.ipynb` in Google Colab
- Upload your dataset or use a public dataset
- Run all cells
- Download the trained model files
- Place `eye_disease_model.keras` in `backend/model/`

### 3. Run Backend

```bash
source venv/bin/activate
cd backend
python main.py
```

API will be available at `http://localhost:8000`

### 4. Run Frontend

```bash
# Terminal 1 (backend already running)
cd backend && python main.py

# Terminal 2 (frontend)
cd frontend && python -m http.server 8001
```

Visit `http://localhost:8001` in your browser

## For End Users

### Prerequisites

- Backend server running
- Trained model loaded

### Using the Web Interface

1. Open the application in your browser
2. Tap the upload area or drag & drop an eye image
3. Preview the uploaded image
4. Click "Analyze Image"
5. View the result:
   - Predicted class
   - Confidence score
   - Explanation

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)

### Mobile Usage

Works on Android browsers (Chrome, Firefox, etc.) without any modifications.

## Testing the API

```bash
# Test with a sample image
python backend/test_api.py path/to/test_image.jpg
```

## Troubleshooting Quick Fixes

### "Model not loaded" error
- Ensure model file exists in `backend/model/`
- Train the model using the Colab notebook

### "Could not connect to API" error
- Check if backend is running (`python backend/main.py`)
- Verify API URL in `frontend/script.js`

### Slow predictions
- Use a smaller image
- Ensure TensorFlow is optimized for CPU
- Consider using TFLite model

## Project Architecture

```
Frontend (Static HTML/CSS/JS)
    ↓ HTTP POST (multipart/form-data)
Backend (FastAPI)
    ↓ Preprocessing
ML Model (TensorFlow/Keras)
    ↓ JSON Response
Frontend (Display Results)
```

## Key Features

- Fast inference (< 10 seconds)
- Mobile-first responsive design
- Scalable modular architecture
- RESTful API
- Support for multiple image formats
- Clear medical disclaimer

## Next Steps

1. Add more eye condition classes
2. Improve dataset quality and quantity
3. Implement user authentication
4. Add batch processing
5. Deploy to production
6. Create mobile app wrapper

For detailed documentation, see `README.md`
