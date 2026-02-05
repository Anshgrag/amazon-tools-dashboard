# app.py
"""
EcoTrack: Electricity and Air Quality Monitoring System
Backend API Server using Flask and SQLite

This is a beginner-friendly REST API that handles:
1. AQI data from Raspberry Pi
2. Electricity data from smart plugs or simulated sources

No authentication required - single dashboard system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

# Initialize Flask application
app = Flask(__name__)

# Enable CORS for all routes (allows frontend to access API)
CORS(app)

# Database file name
DATABASE = 'ecotrack.db'

# ==================== DATABASE FUNCTIONS ====================

def get_db_connection():
    """
    Create a connection to SQLite database
    Returns: sqlite3.Connection object
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn


def init_database():
    """
    Initialize the database and create tables if they don't exist
    Called when the server starts
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create AQI table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aqi_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_type TEXT NOT NULL,
            aqi_value INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    
    # Create Electricity table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS electricity_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            mode TEXT NOT NULL,
            voltage REAL NOT NULL,
            power_watts REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


# ==================== AQI API ENDPOINTS ====================

@app.route('/api/aqi/add', methods=['POST'])
def add_aqi_data():
    """
    Endpoint to receive and store AQI data from Raspberry Pi
    
    Expected JSON format:
    {
        "location_type": "indoor" or "outdoor",
        "aqi_value": 45,
        "timestamp": "2026-01-08T10:30:00"
    }
    
    Returns: Success or error message
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data or 'location_type' not in data or 'aqi_value' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields: location_type and aqi_value'
            }), 400
        
        location_type = data['location_type']
        aqi_value = data['aqi_value']
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO aqi_data (location_type, aqi_value, timestamp)
            VALUES (?, ?, ?)
        ''', (location_type, aqi_value, timestamp))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'AQI data added successfully',
            'data': {
                'location_type': location_type,
                'aqi_value': aqi_value,
                'timestamp': timestamp
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/aqi/latest', methods=['GET'])
def get_latest_aqi():
    """
    Get the most recent AQI reading
    Used by dashboard to display current AQI
    
    Returns: Latest AQI data for indoor and outdoor
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get latest indoor AQI
        cursor.execute('''
            SELECT location_type, aqi_value, timestamp
            FROM aqi_data
            WHERE location_type = 'indoor'
            ORDER BY timestamp DESC
            LIMIT 1
        ''')
        indoor = cursor.fetchone()
        
        # Get latest outdoor AQI
        cursor.execute('''
            SELECT location_type, aqi_value, timestamp
            FROM aqi_data
            WHERE location_type = 'outdoor'
            ORDER BY timestamp DESC
            LIMIT 1
        ''')
        outdoor = cursor.fetchone()
        
        conn.close()
        
        result = {
            'status': 'success',
            'data': {
                'indoor': dict(indoor) if indoor else None,
                'outdoor': dict(outdoor) if outdoor else None
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/aqi/history', methods=['GET'])
def get_aqi_history():
    """
    Get AQI history for graphing
    Optional query parameter: limit (default: 50)
    
    Example: /api/aqi/history?limit=100
    
    Returns: List of AQI readings
    """
    try:
        # Get limit from query parameter (default 50)
        limit = request.args.get('limit', 50, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT location_type, aqi_value, timestamp
            FROM aqi_data
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        history = [dict(row) for row in rows]
        
        return jsonify({
            'status': 'success',
            'count': len(history),
            'data': history
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ==================== ELECTRICITY API ENDPOINTS ====================

@app.route('/api/electricity/add', methods=['POST'])
def add_electricity_data():
    """
    Endpoint to receive and store electricity data
    
    Expected JSON format:
    {
        "device_name": "TV",
        "mode": "ON",
        "voltage": 230.5,
        "power_watts": 85.3,
        "timestamp": "2026-01-08T10:30:00"
    }
    
    Returns: Success or error message
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['device_name', 'mode', 'voltage', 'power_watts']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(required_fields)}'
            }), 400
        
        device_name = data['device_name']
        mode = data['mode']
        voltage = data['voltage']
        power_watts = data['power_watts']
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO electricity_data (device_name, mode, voltage, power_watts, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (device_name, mode, voltage, power_watts, timestamp))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Electricity data added successfully',
            'data': {
                'device_name': device_name,
                'mode': mode,
                'voltage': voltage,
                'power_watts': power_watts,
                'timestamp': timestamp
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/electricity/history', methods=['GET'])
def get_electricity_history():
    """
    Get electricity usage history for all devices
    Optional query parameters:
    - limit: number of records (default: 100)
    - device: filter by device name
    
    Example: /api/electricity/history?limit=50&device=TV
    
    Returns: List of electricity readings
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        device_filter = request.args.get('device', None)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if device_filter:
            # Filter by specific device
            cursor.execute('''
                SELECT device_name, mode, voltage, power_watts, timestamp
                FROM electricity_data
                WHERE device_name = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (device_filter, limit))
        else:
            # Get all devices
            cursor.execute('''
                SELECT device_name, mode, voltage, power_watts, timestamp
                FROM electricity_data
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        history = [dict(row) for row in rows]
        
        return jsonify({
            'status': 'success',
            'count': len(history),
            'data': history
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ==================== UTILITY ENDPOINTS ====================

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint - API health check
    """
    return jsonify({
        'message': 'EcoTrack API is running!',
        'version': '1.0',
        'endpoints': {
            'AQI': [
                'POST /api/aqi/add',
                'GET /api/aqi/latest',
                'GET /api/aqi/history'
            ],
            'Electricity': [
                'POST /api/electricity/add',
                'GET /api/electricity/history'
            ]
        }
    }), 200


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get overall statistics
    Useful for dashboard summary
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Count AQI records
        cursor.execute('SELECT COUNT(*) as count FROM aqi_data')
        aqi_count = cursor.fetchone()['count']
        
        # Count electricity records
        cursor.execute('SELECT COUNT(*) as count FROM electricity_data')
        electricity_count = cursor.fetchone()['count']
        
        # Get unique devices
        cursor.execute('SELECT DISTINCT device_name FROM electricity_data')
        devices = [row['device_name'] for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_aqi_records': aqi_count,
                'total_electricity_records': electricity_count,
                'monitored_devices': devices,
                'device_count': len(devices)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ==================== SERVER STARTUP ====================

if __name__ == '__main__':
    # Initialize database when server starts
    init_database()
    
    # Run the Flask server
    # host='0.0.0.0' makes it accessible from other devices on network
    # port=5000 is the default Flask port
    # debug=True provides helpful error messages (disable in production)
    print("🚀 Starting EcoTrack Backend Server...")
    print("📡 Server will run on: http://localhost:5000")
    print("📊 API Documentation: http://localhost:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)
