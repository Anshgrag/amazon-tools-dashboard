#!/bin/bash

# Eye Disease Detection - Development Setup
echo "🛠️  Setting up development environment..."

# Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi

# Setup Backend
echo "🐍 Setting up Python backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend setup complete"

# Setup Frontend
echo "⚛️  Setting up Node.js frontend..."
cd ../frontend

# Install dependencies
npm install

echo "✅ Frontend setup complete"

# Setup ML Environment
echo "🤖 Setting up ML environment..."
cd ../ml

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install ML dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ ML environment setup complete"

cd ..

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "To run the application:"
echo ""
echo "1. Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. ML Training (Optional - Terminal 3):"
echo "   cd ml"
echo "   source venv/bin/activate"
echo "   python training/train.py"
echo ""
echo "📋 Next steps:"
echo "   - Create PostgreSQL database or use Docker"
echo "   - Add trained model to ml/models/weights/best_model.pth"
echo "   - Set up environment variables in backend/.env"