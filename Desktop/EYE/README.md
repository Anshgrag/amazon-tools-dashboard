# Eye Infection Detection System

A full-stack web application for preliminary eye infection detection using AI. The system analyzes non-microscopic eye photographs to detect potential eye conditions including Normal, Conjunctivitis, Cataract, and Glaucoma.

## Disclaimer

This tool is for preliminary screening only and not a medical diagnosis. Always consult an ophthalmologist for proper diagnosis and treatment.

## Features

- Mobile-first responsive UI (Android browser compatible)
- Image upload with preview (JPEG/PNG support)
- Real-time AI-based prediction
- Fast inference (< 10 seconds on CPU)
- Clear result display with confidence scores
- RESTful API backend
- Scalable architecture for adding new conditions

## Project Structure

```
EYE/
├── frontend/
│   ├── index.html          # Main frontend interface
│   ├── style.css           # Styling (mobile-first)
│   └── script.js            # Frontend logic
├── backend/
│   ├── main.py              # FastAPI application
│   ├── model/               # Trained model files
│   └── utils/
│       ├── preprocessing.py # Image preprocessing utilities
│       └── inference.py     # Model inference wrapper
├── training/
│   └── eye_detection_training.ipynb  # Google Colab training notebook
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Chrome or modern web browser

### 1. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Train the Model

Before running the backend, you need to train the model using the provided notebook:

1. **Prepare Dataset**: Organize your eye images in the following structure:

```
eye_dataset/
├── Normal/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Conjunctivitis/
│   └── ...
├── Cataract/
│   └── ...
└── Glaucoma/
    └── ...
```

2. **Open in Google Colab**:
   - Upload `training/eye_detection_training.ipynb` to Google Colab
   - Update `DATASET_PATH` in the notebook to point to your dataset
   - Run all cells to train the model

3. **Download Model**:
   - After training, download the saved `.keras` and `.h5` model files
   - Place them in `backend/model/` directory

### 3. Run Backend

```bash
# Navigate to backend directory
cd backend

# Start FastAPI server
python main.py
```

The API will be available at `http://localhost:8000`

### 4. Run Frontend

```bash
# Open frontend/index.html in a web browser
# Or use a local server:
cd frontend
python -m http.server 8001
```

Access the application at `http://localhost:8001`

## API Documentation

### Endpoints

#### POST /predict

Predict eye disease from uploaded image.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (image file, JPEG or PNG)

**Response:**
```json
{
  "success": true,
  "predicted_class": "Normal",
  "confidence_score": 0.9543
}
```

**Classes:**
- Normal
- Conjunctivitis
- Cataract
- Glaucoma

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### GET /classes

Get list of supported disease classes.

**Response:**
```json
{
  "classes": ["Normal", "Conjunctivitis", "Cataract", "Glaucoma"]
}
```

## Model Details

### Architecture

- **Base Model**: MobileNetV2 (transfer learning from ImageNet)
- **Input Size**: 224x224 pixels
- **Preprocessing**: Resize, normalize pixel values to [0, 1]
- **Classification Head**: Custom dense layers with dropout for regularization
- **Output**: 4 classes with softmax activation

### Training

- **Framework**: TensorFlow/Keras
- **Optimizer**: Adam with learning rate scheduling
- **Loss Function**: Categorical Crossentropy
- **Metrics**: Accuracy, AUC
- **Data Augmentation**: Rotation, flip, zoom, shift
- **Training Strategy**: Two-phase (frozen base model + fine-tuning)

### Performance

- **Inference Time**: < 10 seconds on CPU
- **Accuracy**: (Depends on training data quality and quantity)
- **Model Size**: ~15 MB (with optimizations)

## Deployment

### Local Development

```bash
# Backend
cd backend
python main.py

# Frontend (new terminal)
cd frontend
python -m http.server 8001
```

### Production Deployment

#### Backend (FastAPI)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Frontend

Serve static files using Nginx, Apache, or deploy to Netlify/Vercel.

### Docker Deployment

```dockerfile
# Dockerfile for backend
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t eye-detection-api .
docker run -p 8000:8000 eye-detection-api
```

## Mobile App Compatibility

The frontend is mobile-first and can be wrapped for Android apps:

### Option 1: WebView

Create an Android app with WebView that loads the frontend URL.

### Option 2: PWA (Progressive Web App)

Add `manifest.json` for PWA support:

```json
{
  "name": "Eye Infection Detection",
  "short_name": "Eye Detect",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#2563eb",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

## Troubleshooting

### Model Not Found Error

```
Warning: Model file not found at backend/model/eye_disease_model.keras
```

**Solution**: Train the model using the notebook and save it to `backend/model/` directory.

### CORS Errors

If you see CORS errors in browser console:

**Solution**: The backend already has CORS enabled. Ensure the backend is running on the correct port.

### Slow Inference

If predictions take longer than 10 seconds:

**Solution**: 
- Use TFLite model (exported by notebook) for faster inference
- Ensure TensorFlow is using CPU optimizations
- Reduce image resolution if acceptable

### Memory Issues

If you run out of memory during training:

**Solution**: 
- Reduce `BATCH_SIZE` in the notebook configuration
- Use a smaller base model (MobileNetV2 instead of EfficientNet)
- Use gradient accumulation

## Future Enhancements

1. **Additional Conditions**: Add detection for more eye conditions
2. **Image Quality Check**: Validate image quality before analysis
3. **Batch Processing**: Analyze multiple images at once
4. **User Authentication**: Add user accounts and history tracking
5. **Multi-language Support**: Add translations for global accessibility
6. **Offline Mode**: PWA with service workers for offline use
7. **Image Segmentation**: Highlight regions of interest in images
8. **Explainable AI**: Add Grad-CAM visualizations to show model focus

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Dataset Sources

For training the model, you can use publicly available datasets:

- **Eye Disease Detection Dataset** (Kaggle)
- **Ocular Disease Recognition** (Kaggle)
- **APOLLO Eye Disease Dataset**
- **Custom collected non-microscopic eye images**

Ensure you have proper rights to use any dataset for training.

## License

This project is for educational and research purposes. Always consult medical professionals for actual diagnosis.

## Support

For issues, questions, or suggestions, please open an issue on the repository.

## Acknowledgments

- TensorFlow/Keras team for the ML framework
- FastAPI team for the web framework
- Medical imaging research community

---

**Remember**: This is a preliminary screening tool and NOT a medical diagnosis. Always consult an ophthalmologist for proper diagnosis and treatment.
