# 🚀 Getting Started with Eye Disease Detection

## Quick Start Options

### 🐳 Option 1: Docker (Recommended - Easiest)
```bash
# Navigate to project
cd "eye project"

# Run automated setup
./scripts/setup.sh

# Check status
cd docker
docker compose ps
```

### 🛠️ Option 2: Local Development
```bash
# Run installation script
./install.sh

# Activate virtual environment
source eye_disease_env/bin/activate

# Start backend (Terminal 1)
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (Terminal 2)
cd frontend  
npm install
npm run dev
```

## 📋 Prerequisites

### Required:
- **Python 3.11+**
- **Node.js 18+** 
- **Docker & Docker Compose** (for Docker setup)

### Optional:
- **PostgreSQL** (can use Docker)
- **Redis** (can use Docker)
- **GPU** (for faster ML inference)

## 🔧 Environment Setup

### Create Environment Files
```bash
# Backend environment
cp backend/.env.example backend/.env
# Edit with your settings

# Frontend environment  
cp frontend/.env.example frontend/.env.local
# Edit with API URL
```

### Key Environment Variables
```env
# Backend (.env)
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/eyedisease
SECRET_KEY=your-secret-key-here
MODEL_PATH=ml/models/weights/best_model.pth

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🗂️ Project Structure
```
eye-disease-detection/
├── backend/           # FastAPI Python API
├── frontend/          # Next.js React app
├── ml/               # PyTorch ML models
├── docker/           # Docker configuration
├── scripts/           # Setup scripts
├── requirements.txt    # All Python dependencies
└── install.sh         # Quick install script
```

## 🧪 Testing Setup

### 1. Check Dependencies
```bash
# Python version
python3 --version

# Node version  
node --version

# Docker version
docker --version
docker compose version
```

### 2. Test Backend
```bash
# Start backend
cd backend
source eye_disease_env/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test API
curl http://localhost:8000/api/v1/health
```

### 3. Test Frontend
```bash
# Start frontend
cd frontend
npm run dev

# Open browser
# Navigate to http://localhost:3000
```

## 🤖 ML Model Setup

### Option A: Use Mock Mode (Default)
- Application works without trained model
- Returns mock predictions for testing
- Perfect for development and UI testing

### Option B: Add Real Model
```bash
# Add your trained model
cp your_model.pth ml/models/weights/best_model.pth

# Or train new model
cd ml
source ../eye_disease_env/bin/activate
python training/train.py
```

## 📊 Access Points

Once running, access:

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Model Status**: http://localhost:8000/api/v1/models/status

## 🔍 Troubleshooting

### Port Already in Use
```bash
# Find what's using port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Kill process
kill -9 <PID>
```

### Dependencies Not Found
```bash
# Install missing system packages
sudo apt-get update
sudo apt-get install python3-dev python3-pip nodejs npm

# Install Python packages
pip install -r requirements.txt
```

### Virtual Environment Issues
```bash
# Create new environment
python3 -m venv eye_disease_env
source eye_disease_env/bin/activate

# Delete and recreate
rm -rf eye_disease_env
python3 -m venv eye_disease_env
```

### Docker Issues
```bash
# Clean up Docker
docker system prune -f

# Rebuild containers
docker compose down
docker compose up --build
```

## 🎯 Next Steps

1. **✅ Run setup** - Use Docker or install locally
2. **🧪 Test** - Verify API and frontend work
3. **📸 Upload images** - Test eye analysis feature
4. **🔧 Customize** - Modify code for your needs
5. **🚀 Deploy** - Use production configuration

## 📞 Getting Help

### Common Issues:
- **Import errors**: Ensure virtual environment is active
- **Port conflicts**: Stop other services using ports 3000/8000
- **Database connection**: Check PostgreSQL is running
- **Model not found**: Add model to `ml/models/weights/` or use mock mode

### Resources:
- **Documentation**: `context.md`, `docs/RUN_GUIDE.md`
- **API Reference**: http://localhost:8000/api/docs
- **Issues**: Report bugs on GitHub
- **Setup Help**: Check `scripts/` directory for automation

---

**🎉 You're ready to start with Eye Disease Detection!**

Choose Docker setup for easiest experience, or local development for full control.