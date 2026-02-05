#!/bin/bash

# Quick Installation Script for Eye Disease Detection
echo "🔧 Setting up Eye Disease Detection Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 Found Python $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv eye_disease_env
source eye_disease_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install main requirements
echo "📥 Installing Python dependencies..."
if [ -f "requirements-free.txt" ]; then
    pip install -r requirements-free.txt
    echo "✅ Dependencies installed from requirements-free.txt"
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed from requirements.txt"
else
    echo "❌ No requirements file found in current directory"
    echo "Please run this script from the project root directory"
    deactivate
    exit 1
fi

# Install backend specific requirements
if [ -d "backend" ] && [ -f "backend/requirements.txt" ]; then
    echo "🔧 Installing backend dependencies..."
    pip install -r backend/requirements.txt
    echo "✅ Backend dependencies installed"
fi

# Install ML specific requirements
if [ -d "ml" ] && [ -f "ml/requirements.txt" ]; then
    echo "🤖 Installing ML dependencies..."
    pip install -r ml/requirements.txt
    echo "✅ ML dependencies installed"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p ml/models/weights
mkdir -p ml/data/processed
mkdir -p uploads
mkdir -p logs

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Keep the virtual environment active: source eye_disease_env/bin/activate"
echo "2. Set up database (PostgreSQL recommended)"
echo "3. Set up environment variables (copy .env.example to .env)"
echo "4. Add trained model to ml/models/weights/best_model.pth (optional)"
echo ""
echo "🚀 To run the application:"
echo ""
echo "Backend (Terminal 1):"
echo "  source eye_disease_env/bin/activate"
echo "  cd backend"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Frontend (Terminal 2 - if using React):"
echo "  cd frontend"
echo "  npm install"
echo "  npm run dev"
echo ""
echo "ML Training (Terminal 3 - optional):"
echo "  source eye_disease_env/bin/activate"
echo "  cd ml"
echo "  python training/train.py"
echo ""
echo "📚 For Docker setup, run: ./scripts/setup.sh"
echo ""
echo "📖 Documentation: Check context.md and docs/RUN_GUIDE.md"