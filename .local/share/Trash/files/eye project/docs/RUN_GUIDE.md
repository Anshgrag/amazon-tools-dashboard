# 🚀 How to Run the Eye Disease Detection Application

## Quick Start Options

### 🐳 Option 1: Docker Compose (Recommended for Production)
```bash
# Clone and navigate to project
cd eye-disease-detection

# Run the automated setup script
./scripts/setup.sh

# Or manually:
cd docker
docker-compose up --build -d
```

**Access URLs:**
- 🌐 Frontend: http://localhost:3000
- 📚 API Docs: http://localhost:8000/api/docs
- 📊 Monitoring: http://localhost:3001 (Grafana)
- 🔍 Metrics: http://localhost:9090 (Prometheus)

---

### 🛠️ Option 2: Local Development (Recommended for Development)
```bash
# Run the development setup script
./scripts/dev-setup.sh

# Then start services manually (see detailed steps below)
```

---

## 📋 Detailed Setup Instructions

### Prerequisites
- **Docker & Docker Compose** (for Option 1)
- **Python 3.11+** (for Option 2)
- **Node.js 18+** (for Option 2)
- **PostgreSQL** (if running locally without Docker)
- **Git**

---

## 🐳 Docker Compose Setup (Step-by-Step)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd eye-disease-detection
```

### 2. Run Setup Script
```bash
./scripts/setup.sh
```

This script will:
- ✅ Create necessary directories
- ✅ Set up environment files
- ✅ Configure Nginx, Prometheus, Grafana
- ✅ Build and start all containers
- ✅ Check service health

### 3. Verify Services
```bash
# Check all containers are running
docker-compose ps

# Check logs if needed
docker-compose logs backend
docker-compose logs frontend
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/v1/health

---

## 🛠️ Local Development Setup (Step-by-Step)

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database settings

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with API URL

# Start the frontend server
npm run dev
```

### 3. Database Setup (PostgreSQL)
```bash
# Using Docker for database only
docker run -d \
  --name postgres \
  -e POSTGRES_DB=eyedisease \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres123 \
  -p 5432:5432 \
  postgres:15-alpine

# Or install PostgreSQL locally
# Create database: eyedisease
# User: postgres, Password: postgres123
```

### 4. Redis Setup (Optional, for caching)
```bash
# Using Docker
docker run -d --name redis -p 6379:6379 redis:7-alpine

# Or install Redis locally
```

---

## 🤖 ML Model Setup

### Option A: Use Pre-trained Model
```bash
# Download a pre-trained model (placeholder)
# Add to: ml/models/weights/best_model.pth

# For testing without model, the API will return mock responses
```

### Option B: Train Your Own Model
```bash
cd ml

# Setup ML environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Prepare dataset (add images to ml/data/)
# Create labels.csv with image_path and label columns

# Train the model
python training/train.py

# Model will be saved to ml/models/checkpoints/
# Copy best model to ml/models/weights/best_model.pth
```

---

## 📊 Environment Configuration

### Backend Environment (.env)
```env
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/eyedisease
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-this
DEBUG=true
MODEL_PATH=ml/models/weights/best_model.pth
ALLOWED_ORIGINS=["http://localhost:3000"]
```

### Frontend Environment (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## 🧪 Testing the Application

### 1. Test API Endpoints
```bash
# Health check
curl http://localhost:8000/api/v1/health

# API documentation
# Open http://localhost:8000/api/docs in browser
```

### 2. Test Frontend
```bash
# Open http://localhost:3000 in browser
# Test image upload functionality
```

### 3. Test ML Pipeline
```bash
# Test model inference
cd ml
python -c "
from models.cnn_vit_hybrid import EyeDiseasePredictor
from PIL import Image
import torch

# Test with dummy image (if model exists)
try:
    predictor = EyeDiseasePredictor('ml/models/weights/best_model.pth')
    print('Model loaded successfully')
except:
    print('Model not found - using mock responses')
"
```

---

## 🔧 Common Issues & Solutions

### Issue: Backend fails to start
**Solution:**
```bash
# Check if port 8000 is free
lsof -i :8000

# Kill any process using port 8000
kill -9 <PID>

# Check database connection
docker-compose logs postgres
```

### Issue: Frontend fails to start
**Solution:**
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check if port 3000 is free
lsof -i :3000
```

### Issue: Model not found
**Solution:**
```bash
# The application will work with mock responses
# To use real model, add trained model to:
ml/models/weights/best_model.pth
```

### Issue: Database connection failed
**Solution:**
```bash
# Check PostgreSQL container
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

---

## 📱 Accessing the Application

### Main Features
1. **Welcome Screen**: Overview and medical disclaimer
2. **User Authentication**: Register/login
3. **Image Upload**: Camera or gallery upload
4. **Analysis Results**: AI predictions with confidence
5. **Scan History**: Previous results tracking

### API Endpoints
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/analysis/analyze` - Upload and analyze image
- `GET /api/v1/analysis/results/{id}` - Get results
- `GET /api/v1/health` - Health check

---

## 🔍 Monitoring & Debugging

### Check Logs
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Application logs
tail -f backend/app.log
```

### Monitoring Dashboards
- **Grafana**: http://localhost:3001 (admin/admin123)
- **Prometheus**: http://localhost:9090
- **API Metrics**: http://localhost:8000/metrics

---

## 🚀 Production Deployment

### For Production Use:
1. **Change default passwords** in environment files
2. **Add SSL certificates** for HTTPS
3. **Set up proper domain** and DNS
4. **Configure backup** for database
5. **Add monitoring alerts**
6. **Scale services** as needed

### Docker Production Commands
```bash
# Build production images
docker-compose -f docker/docker-compose.yml build

# Deploy to production
docker-compose -f docker/docker-compose.yml up -d

# Scale services
docker-compose -f docker/docker-compose.yml up -d --scale backend=3
```

---

## 🆘 Getting Help

### Resources
- 📖 **Documentation**: Check `context.md` for detailed architecture
- 🐛 **Issues**: Report bugs on GitHub Issues
- 📧 **Support**: Contact development team

### Troubleshooting Checklist
- ✅ All prerequisites installed
- ✅ Environment variables set correctly
- ✅ Database running and accessible
- ✅ Ports not blocked by firewall
- ✅ Sufficient disk space and memory

---

**🎉 You're now ready to run the Eye Disease Detection Application!**

Start with the Docker Compose setup for the easiest experience, or use the local development setup if you want to modify the code.