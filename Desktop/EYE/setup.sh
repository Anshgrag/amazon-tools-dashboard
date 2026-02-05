#!/bin/bash
# Setup script for Eye Infection Detection System

echo "=========================================="
echo "Eye Infection Detection System Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Train the model using Google Colab:"
echo "   - Open training/eye_detection_training.ipynb"
echo "   - Run all cells to train the model"
echo "   - Download the trained .keras and .h5 files"
echo "   - Place them in backend/model/ directory"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   python main.py"
echo ""
echo "3. Open the frontend:"
echo "   - Open frontend/index.html in your browser"
echo "   - Or run: cd frontend && python -m http.server 8001"
echo ""
echo "For more details, see README.md"
