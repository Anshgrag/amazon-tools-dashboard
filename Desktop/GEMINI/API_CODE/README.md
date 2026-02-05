# EcoTrack API Code

This folder contains the complete EcoTrack energy monitoring system with Tuya smart plug integration.

## Structure

- `backend/` - Flask API server with Tuya integration
- `frontend/` - Web dashboard for energy monitoring
- `tinytuya.json` - Tuya API credentials
- `tuya.py` - Simple Tuya device control script
- `requirements.txt` - Python dependencies

## Setup Instructions

### 1. Backend Setup
```bash
cd backend
source venv/bin/activate
pip install -r ../requirements.txt
python app.py
```

### 2. Frontend Setup
```bash
cd frontend
python3 -m http.server 8000
```

### 3. Tuya Integration
```bash
cd backend
source venv/bin/activate
python tuya_integration.py
```

## Features

- Real-time power monitoring from Tuya smart plugs
- Energy consumption tracking and cost analysis
- Device control (on/off toggle)
- Dashboard with charts and statistics
- Room-based usage analysis
- Savings calculations

## API Endpoints

- `GET /api/electricity/history` - Get electricity data
- `POST /api/electricity/add` - Add electricity reading
- `GET /api/savings` - Get savings data
- `POST /api/devices/{id}/toggle` - Control device
- `GET /api/devices` - Get device list
- `GET /api/stats` - Get system statistics

## Access

- Frontend Dashboard: http://localhost:8000
- Backend API: http://localhost:5000

## Notes

- Ensure `tinytuya.json` contains valid Tuya API credentials
- The system automatically creates `ecotrack.db` database on first run
- Data refreshes every 30 seconds on the frontend
- Tuya integration fetches data every 60 seconds