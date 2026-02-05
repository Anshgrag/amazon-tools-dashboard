from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000'])

DATABASE = 'ecotrack.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS electricity_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            mode TEXT NOT NULL,
            voltage REAL NOT NULL,
            power_watts REAL NOT NULL,
            timestamp TEXT NOT NULL,
            auto_controlled BOOLEAN DEFAULT FALSE,
            manual_override BOOLEAN DEFAULT FALSE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            event_type TEXT NOT NULL,
            power_watts REAL NOT NULL,
            duration_minutes INTEGER NOT NULL,
            cost_wasted REAL NOT NULL,
            timestamp TEXT NOT NULL,
            auto_saved BOOLEAN DEFAULT FALSE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


        
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
        auto_controlled = data.get('auto_controlled', False)
        manual_override = data.get('manual_override', False)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO electricity_data (device_name, mode, voltage, power_watts, timestamp, auto_controlled, manual_override)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (device_name, mode, voltage, power_watts, timestamp, auto_controlled, manual_override))
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
        period = request.args.get('period', 'month')
        limit = request.args.get('limit', 100, type=int)
        device_filter = request.args.get('device', None)
        
        print(f"=== ELECTRICITY API CALLED WITH PERIOD: {period} ===")
        
        # Determine date filter based on period
        date_filter = "timestamp >= datetime('now', '-24 hours')"
        if period == 'today':
            date_filter = "timestamp >= datetime('now', '-24 hours')"
        elif period == 'month':
            date_filter = "timestamp >= datetime('now', 'start of month')"
        elif period == 'year':
            date_filter = "timestamp >= datetime('now', 'start of year')"
        else:
            date_filter = "timestamp >= datetime('now', '-30 days')"
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if device_filter:
            cursor.execute(f'''
                SELECT device_name, mode, voltage, power_watts, timestamp
                FROM electricity_data
                WHERE device_name = ? AND {date_filter}
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (device_filter, limit))
        else:
            cursor.execute(f'''
                SELECT device_name, mode, voltage, power_watts, timestamp
                FROM electricity_data
                WHERE {date_filter}
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        print(f"Found {len(rows)} records for period: {period}")
        
        # Clean data and handle negative power values
        history = []
        for row in rows:
            data = dict(row)
            # Ensure power_watts is not negative (sensor readings can be inaccurate)
            if data['power_watts'] < 0:
                data['power_watts'] = 0
            history.append(data)
        
        return jsonify({
            'status': 'success',
            'count': len(history),
            'period': period,
            'data': history
        }), 200
        
    except Exception as e:
        print(f"Error in electricity history: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'EcoTrack API is running!',
        'version': '1.0',
        'endpoints': {
            'Electricity': [
                'POST /api/electricity/add',
                'GET /api/electricity/history'
            ],
            'Savings': [
                'GET /api/savings',
                'POST /api/device-event'
            ]
        }
    }), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM electricity_data')
        electricity_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT DISTINCT device_name FROM electricity_data')
        devices = [row['device_name'] for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_electricity_records': electricity_count,
                'monitored_devices': devices,
                'device_count': len(devices)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/savings', methods=['GET'])
def get_savings():
    try:
        period = request.args.get('period', 'month')
        print(f"=== SAVINGS API CALLED WITH PERIOD: {period} ===")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Determine date filter based on period
        if period == 'today':
            date_filter = "timestamp >= datetime('now', '-24 hours')"
        elif period == 'month':
            date_filter = "timestamp >= datetime('now', 'start of month')"
        elif period == 'year':
            date_filter = "timestamp >= datetime('now', 'start of year')"
        else:
            date_filter = "timestamp >= datetime('now', '-30 days')"
        
        print(f"Using date filter for period '{period}': {date_filter}")
        
        # Check if we have data for the period
        cursor.execute(f'SELECT COUNT(*) as count FROM electricity_data WHERE {date_filter}')
        data_count = cursor.fetchone()['count']
        
        if data_count == 0:
            return jsonify({
                'status': 'success',
                'data': {
                    'total_waste_cost': 0,
                    'total_saved_cost': 0,
                    'net_savings': 0,
                    'cost_per_kwh': 0.12,
                    'device_details': []
                }
            }), 200
        
        # Calculate waste and savings
        cursor.execute(f'''
            SELECT 
                device_name,
                SUM(CASE WHEN auto_controlled = FALSE AND power_watts > 5 THEN power_watts ELSE 0 END) as waste_power,
                SUM(CASE WHEN auto_controlled = TRUE THEN power_watts ELSE 0 END) as saved_power,
                COUNT(*) as total_readings
            FROM electricity_data 
            WHERE {date_filter}
            GROUP BY device_name
        ''')
        
        devices_data = cursor.fetchall()
        
        # Calculate monetary values (assuming $0.12 per kWh)
        cost_per_kwh = 0.12  # Default: $0.12 per kWh, can be made configurable
        total_waste = 0
        total_saved = 0
        device_details = []
        
        for device in devices_data:
            waste_power = device['waste_power']
            saved_power = device['saved_power']
            
            # Convert to kWh (assuming readings are per hour)
            waste_kwh = (waste_power / 1000) * 24
            saved_kwh = (saved_power / 1000) * 24
            
            waste_cost = waste_kwh * cost_per_kwh
            saved_cost = saved_kwh * cost_per_kwh
            
            total_waste += waste_cost
            total_saved += saved_cost
            
            device_details.append({
                'device_name': device['device_name'],
                'waste_cost': round(waste_cost, 2),
                'saved_cost': round(saved_cost, 2),
                'waste_power': round(waste_power, 2),
                'saved_power': round(saved_power, 2)
            })
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_waste_cost': round(total_waste, 2),
                'total_saved_cost': round(total_saved, 2),
                'net_savings': round(total_saved - total_waste, 2),
                'cost_per_kwh': cost_per_kwh,
                'device_details': device_details
            }
        }), 200
        
    except Exception as e:
        print(f"Error in get_savings: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/device-event', methods=['POST'])
def add_device_event():
    try:
        data = request.get_json()
        
        required_fields = ['device_name', 'event_type', 'power_watts', 'duration_minutes']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400
        
        device_name = data['device_name']
        event_type = data['event_type']  # 'waste' or 'saved'
        power_watts = data['power_watts']
        duration_minutes = data['duration_minutes']
        timestamp = data.get('timestamp', datetime.now().isoformat())
        auto_saved = data.get('auto_saved', False)
        
        # Calculate cost wasted
        cost_per_kwh = 0.12
        power_kw = power_watts / 1000
        duration_hours = duration_minutes / 60
        cost_wasted = power_kw * duration_hours * cost_per_kwh
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO device_events (device_name, event_type, power_watts, duration_minutes, cost_wasted, timestamp, auto_saved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (device_name, event_type, power_watts, duration_minutes, cost_wasted, timestamp, auto_saved))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Device event recorded successfully',
            'cost_wasted': round(cost_wasted, 4)
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    init_database()
    print("🚀 Starting EcoTrack Backend Server...")
    print("📡 Server running on: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
