from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import tinytuya
import json

app = Flask(__name__)
CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000'])

DATABASE = 'ecotrack.db'

# Load Tuya credentials
try:
    with open('../tinytuya.json', 'r') as f:
        tuya_config = json.load(f)
    TUYA_API_KEY = tuya_config['apiKey']
    TUYA_API_SECRET = tuya_config['apiSecret']
    TUYA_API_REGION = tuya_config['apiRegion']
    TUYA_DEVICE_ID = tuya_config['apiDeviceID']
except FileNotFoundError:
    print("❌ tinytuya.json not found")
    TUYA_API_KEY = None

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
            manual_override BOOLEAN DEFAULT FALSE,
            device_type TEXT DEFAULT 'unknown',
            rated_power REAL DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT UNIQUE NOT NULL,
            device_type TEXT NOT NULL,
            rated_power REAL NOT NULL,
            sleep_threshold REAL NOT NULL,
            created_at TEXT NOT NULL
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


        
def get_device_profile(device_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT device_type, rated_power, sleep_threshold FROM device_profiles WHERE device_name = ?', (device_name,))
    profile = cursor.fetchone()
    conn.close()
    return dict(profile) if profile else None

def detect_device_mode(device_name, power_watts):
    profile = get_device_profile(device_name)
    if not profile:
        return 'unknown'
    
    rated_power = profile['rated_power']
    sleep_threshold = profile['sleep_threshold']
    
    if power_watts >= rated_power * 0.8:
        return 'active'
    elif power_watts <= sleep_threshold:
        return 'sleep'
    else:
        return 'standby'

@app.route('/api/device-profile', methods=['POST'])
def add_device_profile():
    try:
        data = request.get_json()
        required_fields = ['device_name', 'device_type', 'rated_power', 'sleep_threshold']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO device_profiles (device_name, device_type, rated_power, sleep_threshold, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['device_name'], data['device_type'], data['rated_power'], data['sleep_threshold'], datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Device profile added'}), 201
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
        auto_controlled = data.get('auto_controlled', False)
        manual_override = data.get('manual_override', False)
        
        profile = get_device_profile(device_name)
        device_type = profile['device_type'] if profile else 'unknown'
        rated_power = profile['rated_power'] if profile else 0
        
        detected_mode = detect_device_mode(device_name, power_watts)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO electricity_data (device_name, mode, voltage, power_watts, timestamp, auto_controlled, manual_override, device_type, rated_power)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (device_name, detected_mode, voltage, power_watts, timestamp, auto_controlled, manual_override, device_type, rated_power))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Electricity data added successfully',
            'detected_mode': detected_mode
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
        
        # Calculate savings based on sleep mode detection and auto-control
        cursor.execute(f'''
            SELECT 
                device_name,
                device_type,
                rated_power,
                SUM(CASE WHEN mode = 'sleep' AND auto_controlled = FALSE THEN power_watts ELSE 0 END) as sleep_waste_power,
                SUM(CASE WHEN mode = 'sleep' AND auto_controlled = TRUE THEN power_watts ELSE 0 END) as sleep_saved_power,
                SUM(CASE WHEN mode = 'active' THEN power_watts ELSE 0 END) as active_power,
                SUM(CASE WHEN mode = 'standby' THEN power_watts ELSE 0 END) as standby_power,
                COUNT(*) as total_readings,
                COUNT(CASE WHEN mode = 'sleep' THEN 1 END) as sleep_readings,
                COUNT(CASE WHEN auto_controlled = TRUE THEN 1 END) as auto_controlled_readings
            FROM electricity_data 
            WHERE {date_filter}
            GROUP BY device_name, device_type, rated_power
        ''')
        
        devices_data = cursor.fetchall()
        
        cost_per_kwh = 0.12
        total_waste = 0
        total_saved = 0
        device_details = []
        
        for device in devices_data:
            device_name = device['device_name']
            device_type = device['device_type']
            rated_power = device['rated_power']
            
            sleep_waste_power = device['sleep_waste_power']
            sleep_saved_power = device['sleep_saved_power']
            active_power = device['active_power']
            standby_power = device['standby_power']
            sleep_readings = device['sleep_readings']
            total_readings = device['total_readings']
            
            # Calculate potential waste if device was left in sleep mode without auto-control
            # Assume each reading represents 1 hour
            sleep_hours_without_control = sleep_readings
            sleep_hours_with_control = device['auto_controlled_readings']
            
            # Calculate actual consumption in sleep mode
            actual_sleep_consumption = (sleep_waste_power + sleep_saved_power) / 1000  # Convert to kWh
            
            # Calculate what would have been consumed without auto-control
            # (device would have stayed in sleep mode for all sleep hours)
            potential_sleep_consumption = (sleep_waste_power / 1000) if sleep_waste_power > 0 else (rated_power * 0.1 / 1000 * sleep_hours_without_control)
            
            # Calculate savings from turning off devices in sleep mode
            sleep_savings_kwh = max(0, potential_sleep_consumption - actual_sleep_consumption)
            sleep_savings_cost = sleep_savings_kwh * cost_per_kwh
            
            # Calculate waste from devices left in sleep/standby without auto-control
            waste_kwh = (sleep_waste_power + standby_power) / 1000
            waste_cost = waste_kwh * cost_per_kwh
            
            total_waste += waste_cost
            total_saved += sleep_savings_cost
            
            device_details.append({
                'device_name': device_name,
                'device_type': device_type,
                'rated_power': rated_power,
                'sleep_waste_cost': round(waste_cost, 2),
                'sleep_saved_cost': round(sleep_savings_cost, 2),
                'sleep_hours_detected': sleep_readings,
                'auto_controlled_hours': device['auto_controlled_readings'],
                'active_power': round(active_power, 2),
                'standby_power': round(standby_power, 2),
                'efficiency_percentage': round((sleep_savings_cost / max(waste_cost + sleep_savings_cost, 0.01)) * 100, 1) if (waste_cost + sleep_savings_cost) > 0 else 0
            })
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_waste_cost': round(total_waste, 2),
                'total_saved_cost': round(total_saved, 2),
                'net_savings': round(total_saved - total_waste, 2),
                'cost_per_kwh': cost_per_kwh,
                'device_details': device_details,
                'calculation_method': 'sleep_mode_detection'
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
        event_type = data['event_type']
        power_watts = data['power_watts']
        duration_minutes = data['duration_minutes']
        timestamp = data.get('timestamp', datetime.now().isoformat())
        auto_saved = data.get('auto_saved', False)
        
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

@app.route('/api/rooms/usage', methods=['GET'])
def get_rooms_usage():
    try:
        period = request.args.get('period', 'month')
        print(f"=== ROOMS API CALLED WITH PERIOD: {period} ===")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if period == 'today':
            date_filter = "timestamp >= datetime('now', '-24 hours')"
        elif period == 'month':
            date_filter = "timestamp >= datetime('now', 'start of month')"
        elif period == 'year':
            date_filter = "timestamp >= datetime('now', 'start of year')"
        else:
            date_filter = "timestamp >= datetime('now', '-30 days')"
        
        cursor.execute(f'''
            SELECT device_name, SUM(power_watts) as total_power
            FROM electricity_data
            WHERE {date_filter}
            GROUP BY device_name
        ''')
        
        rows = cursor.fetchall()
        
        # Get actual devices from database
        cursor.execute('SELECT DISTINCT device_name FROM electricity_data')
        actual_devices = [row['device_name'] for row in cursor.fetchall()]
        
        # Only map devices that actually exist
        room_devices = {
            'living-room': [],
            'kitchen': [],
            'bedroom': [],
            'office': []
        }
        
        conn.close()
        
        room_usage = {
            'living-room': 0,
            'kitchen': 0,
            'bedroom': 0,
            'office': 0
        }
        
        for row in rows:
            device_name = row['device_name']
            total_power = row['total_power']
            
            for room, devices in room_devices.items():
                if device_name in devices:
                    room_usage[room] += total_power
        
        room_details = []
        for room, usage in room_usage.items():
            room_details.append({
                'room': room,
                'room_name': room.replace('-', ' ').title(),
                'usage_kwh': round(usage / 1000, 2)
            })
        
        return jsonify({
            'status': 'success',
            'period': period,
            'data': {
                'rooms': room_usage,
                'details': room_details
            }
        }), 200
        
    except Exception as e:
        print(f"Error in rooms usage: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/devices', methods=['GET'])
def get_devices():
    try:
        print("=== DEVICES API CALLED ===")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get only devices that actually have data
        cursor.execute('''
            SELECT DISTINCT device_name, device_type, rated_power,
                   MAX(CASE WHEN mode = 'active' THEN power_watts ELSE 0 END) as latest_power
            FROM electricity_data 
            GROUP BY device_name, device_type, rated_power
            ORDER BY device_name
        ''')
        
        device_rows = cursor.fetchall()
        conn.close()
        
        devices = []
        for row in device_rows:
            device_name = row['device_name']
            device_type = row['device_type'] or 'unknown'
            rated_power = row['rated_power'] or 0
            latest_power = row['latest_power'] or 0
            
            # Determine status based on power
            status = 'on' if latest_power > 5 else 'off'
            
            devices.append({
                'id': len(devices) + 1,
                'name': device_name,
                'type': device_type,
                'status': status,
                'power': latest_power,
                'room': 'unknown',  # Will be determined by actual device location
                'scheduled': False
            })
        
        return jsonify({
            'status': 'success',
            'data': {
                'devices': devices,
                'schedules': []
            }
        }), 200
        
    except Exception as e:
        print(f"Error in devices: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/devices/<int:device_id>/toggle', methods=['POST'])
def toggle_device(device_id):
    try:
        print(f"=== TOGGLE DEVICE {device_id} ===")
        data = request.get_json()
        state = data.get('state', 'on')  # 'on' or 'off'

        if not TUYA_API_KEY:
            return jsonify({'status': 'error', 'message': 'Tuya credentials not loaded'}), 500

        # Connect to Tuya Cloud
        cloud = tinytuya.Cloud(apiRegion=TUYA_API_REGION, apiKey=TUYA_API_KEY, apiSecret=TUYA_API_SECRET)

        # Send command
        command_value = True if state == 'on' else False
        commands = {"commands": [{"code": "switch_1", "value": command_value}]}
        print(f"Sending command: {commands}")
        response = cloud.sendcommand(TUYA_DEVICE_ID, commands)
        print(f"Tuya response: {response}")

        if response and response.get('success'):
            print(f"✅ Device {device_id} turned {state}")
            return jsonify({
                'status': 'success',
                'message': f'Device {device_id} turned {state}'
            }), 200
        else:
            print(f"❌ Failed to control device: {response}")
            return jsonify({'status': 'error', 'message': f'Failed to control device: {response}'}), 500

    except Exception as e:
        print(f"Error toggling device: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    init_database()
    print("🚀 Starting EcoTrack Backend Server...")
    print("📡 Server running on: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
