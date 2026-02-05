from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'ecotrack.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aqi_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_type TEXT NOT NULL,
            aqi_value INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    
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

@app.route('/api/aqi/add', methods=['POST'])
def add_aqi_data():
    try:
        data = request.get_json()
        
        if not data or 'location_type' not in data or 'aqi_value' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400
        
        location_type = data['location_type']
        aqi_value = data['aqi_value']
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
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
            'message': 'AQI data added successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/aqi/latest', methods=['GET'])
def get_latest_aqi():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT location_type, aqi_value, timestamp
            FROM aqi_data
            WHERE location_type = 'indoor'
            ORDER BY timestamp DESC
            LIMIT 1
        ''')
        indoor = cursor.fetchone()
        
        cursor.execute('''
            SELECT location_type, aqi_value, timestamp
            FROM aqi_data
            WHERE location_type = 'outdoor'
            ORDER BY timestamp DESC
            LIMIT 1
        ''')
        outdoor = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': {
                'indoor': dict(indoor) if indoor else None,
                'outdoor': dict(outdoor) if outdoor else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/aqi/history', methods=['GET'])
def get_aqi_history():
    try:
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
        
        history = [dict(row) for row in rows]
        
        return jsonify({
            'status': 'success',
            'count': len(history),
            'data': history
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/electricity/add', methods=['POST'])
def add_electricity_data():
    try:
        data = request.get_json()
        
        required_fields = ['device_name', 'mode', 'voltage', 'power_watts']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400
        
        device_name = data['device_name']
        mode = data['mode']
        voltage = data['voltage']
        power_watts = data['power_watts']
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
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
            'message': 'Electricity data added successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/electricity/history', methods=['GET'])
def get_electricity_history():
    try:
        limit = request.args.get('limit', 100, type=int)
        device_filter = request.args.get('device', None)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if device_filter:
            cursor.execute('''
                SELECT device_name, mode, voltage, power_watts, timestamp
                FROM electricity_data
                WHERE device_name = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (device_filter, limit))
        else:
            cursor.execute('''
                SELECT device_name, mode, voltage, power_watts, timestamp
                FROM electricity_data
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = [dict(row) for row in rows]
        
        return jsonify({
            'status': 'success',
            'count': len(history),
            'data': history
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
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
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM aqi_data')
        aqi_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM electricity_data')
        electricity_count = cursor.fetchone()['count']
        
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
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    init_database()
    print("🚀 Starting EcoTrack Backend Server...")
    print("📡 Server running on: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
